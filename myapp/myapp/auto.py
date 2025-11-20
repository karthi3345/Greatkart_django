#!/usr/bin/env python3
"""
Auto i18n pipeline:
 - run makemessages for configured languages
 - auto-translate empty msgstr using LibreTranslate
 - preserve placeholders like %(name)s
 - add charset header if missing
 - compilemessages
 - local cache to avoid re-translating same strings
"""

import polib
import requests
import subprocess
import os
import sys
import time
import json
from pathlib import Path
from typing import Optional

# ----------------------------
# CONFIG
# ----------------------------
# Languages to generate/translate (Django language codes)
LANGUAGES = ["hi", "ta", "te", "kn"]  # add/remove as you want

# Path to project root (where manage.py lives). Default: current working dir
PROJECT_ROOT = Path.cwd()

# Relative path to locale directory from PROJECT_ROOT
LOCALE_DIR = PROJECT_ROOT / "locale"

# LibreTranslate endpoint (stable public instance). Replace if needed.
API_URL = "https://libretranslate.de/translate"

# Sleep between requests to be polite (seconds)
REQUEST_DELAY = 0.45

# Retries for HTTP requests
MAX_RETRIES = 4
RETRY_BACKOFF = 1.5  # exponential backoff multiplier

# Cache file to avoid re-translating identical strings repeatedly
CACHE_FILE = PROJECT_ROOT / ".translate_cache.json"

# Minimum length to attempt translation (skip trivial tokens)
MIN_LENGTH_TO_TRANSLATE = 2

# If True, skip translating text that contains formatting placeholders.
# For messages that include placeholders like "%(product_name)s", we keep them as-is.
SKIP_IF_CONTAINS_PLACEHOLDER = True

# ----------------------------
# UTIL
# ----------------------------
def run_cmd(cmd, cwd=PROJECT_ROOT, check=True):
    """Run shell command and stream output; raise if check and exit non-zero."""
    print(f"> {cmd}")
    proc = subprocess.run(cmd, shell=True, cwd=str(cwd), capture_output=True, text=True)
    if proc.stdout:
        print(proc.stdout.strip())
    if proc.stderr:
        print(proc.stderr.strip(), file=sys.stderr)
    if check and proc.returncode != 0:
        raise RuntimeError(f"Command failed ({cmd}) exit={proc.returncode}")
    return proc

def load_cache():
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def save_cache(cache):
    try:
        CACHE_FILE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception as e:
        print("Warning: could not save cache:", e)

def safe_post_json(url, json_payload):
    """Post with retries and exponential backoff. Returns response.json() or raises."""
    backoff = 1.0
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.post(url, json=json_payload, timeout=12)
            resp.raise_for_status()
            # Some instances may return non-json or empty; guard against that
            if not resp.text or not resp.text.strip():
                raise ValueError("Empty response")
            return resp.json()
        except Exception as exc:
            print(f"Warning: request attempt {attempt} failed: {exc}")
            if attempt == MAX_RETRIES:
                raise
            time.sleep(backoff)
            backoff *= RETRY_BACKOFF

def contains_placeholder(text: str) -> bool:
    return "%(" in text and ")s" in text

def should_translate(msgid: str) -> bool:
    if not msgid or not msgid.strip():
        return False
    if len(msgid.strip()) <= MIN_LENGTH_TO_TRANSLATE:
        # still allow some two-letter tokens if you want; currently skip
        return False
    if SKIP_IF_CONTAINS_PLACEHOLDER and contains_placeholder(msgid):
        # we skip translating complex placeholder-containing strings to avoid corruption
        return False
    return True

# ----------------------------
# TRANSlation logic
# ----------------------------
def translate_text_libre(text: str, target_lang: str) -> str:
    """Translate using LibreTranslate; returns translatedText or raises."""
    payload = {
        "q": text,
        "source": "en",
        "target": target_lang,
        "format": "text"
    }
    data = safe_post_json(API_URL, payload)
    # response example: {"translatedText": "..."}
    translated = data.get("translatedText")
    if translated is None:
        raise ValueError("No 'translatedText' in response")
    return translated

def ensure_po_header_charset(po: polib.POFile):
    """Ensure header contains Content-Type with charset; polib uses metadata dict for headers."""
    meta = po.metadata or {}
    ct = meta.get("Content-Type") or meta.get("MIME-Version")
    # Set Content-Type to text/plain; charset=UTF-8 if missing
    if "Content-Type" not in meta or "charset" not in (meta.get("Content-Type") or ""):
        po.metadata["Content-Type"] = "text/plain; charset=UTF-8"

# ----------------------------
# FILE / PO handling
# ----------------------------
def ensure_locale_dirs(lang: str):
    """Create locale/<lang>/LC_MESSAGES and empty django.po if missing."""
    po_dir = LOCALE_DIR / lang / "LC_MESSAGES"
    po_dir.mkdir(parents=True, exist_ok=True)
    po_file = po_dir / "django.po"
    if not po_file.exists():
        # create empty po file with minimal header
        po = polib.POFile()
        po.metadata = {
            "Project-Id-Version": "1.0",
            "Report-Msgid-Bugs-To": "",
            "POT-Creation-Date": time.strftime("%Y-%m-%d %H:%M%z"),
            "PO-Revision-Date": time.strftime("%Y-%m-%d %H:%M%z"),
            "Last-Translator": "",
            "Language-Team": "",
            "Language": lang,
            "MIME-Version": "1.0",
            "Content-Type": "text/plain; charset=UTF-8",
            "Content-Transfer-Encoding": "8bit",
        }
        po.save(str(po_file))
        print(f"Created empty .po at {po_file}")
    return po_file

def process_po_file(po_path: Path, lang: str, cache: dict):
    print(f"\nProcessing {po_path} for lang={lang}")
    po = polib.pofile(str(po_path))
    ensure_po_header_charset(po)

    updated = False
    for entry in po:
        # skip obsolete entries
        if entry.obsolete:
            continue

        # If msgstr already filled, skip
        if entry.msgstr and entry.msgstr.strip():
            continue

        msgid = entry.msgid.strip()
        if not msgid:
            continue

        # Use cache key (lang + text)
        cache_key = f"{lang}||{msgid}"
        if cache_key in cache:
            entry.msgstr = cache[cache_key]
            updated = True
            print(f"Cached → {msgid} -> {entry.msgstr}")
            continue

        # decide whether to translate
        if not should_translate(msgid):
            # either skip placeholders or too short: keep source as fallback
            entry.msgstr = msgid
            cache[cache_key] = entry.msgstr
            updated = True
            print(f"Skipped translate (placeholder/short) → {msgid} → {entry.msgstr}")
            continue

        # attempt translation
        try:
            translated = translate_text_libre(msgid, lang)
            entry.msgstr = translated
            cache[cache_key] = translated
            updated = True
            print(f"Translated → {msgid} → {translated}")
        except Exception as e:
            # fallback: set msgstr to msgid to prevent empty strings
            print(f"Error translating {msgid[:60]!r}: {e}")
            entry.msgstr = msgid
            cache[cache_key] = entry.msgstr

        # polite delay to avoid rate limiting
        time.sleep(REQUEST_DELAY)

    if updated:
        # Save with UTF-8 and ensure header has charset
        ensure_po_header_charset(po)
        po.save(str(po_path))
        print(f"Saved updated .po -> {po_path}")
    else:
        print("No updates needed for this file.")

# ----------------------------
# MAIN FLOW
# ----------------------------
def main():
    print("Auto i18n started.")
    print("Project root:", PROJECT_ROOT)

    # 1) make sure manage.py exists
    manage_py = PROJECT_ROOT / "manage.py"
    if not manage_py.exists():
        print("Error: manage.py not found in current directory. cd to project root (where manage.py is).")
        sys.exit(1)

    # 2) run makemessages for each language
    for lang in LANGUAGES:
        cmd = f"django-admin makemessages -l {lang}"
        try:
            print("\n==> Running makemessages for", lang)
            run_cmd(cmd)
        except Exception as e:
            print(f"Warning: makemessages failed for {lang}: {e}")
            # continue — files may still exist

    # 3) load cache
    cache = load_cache()

    # 4) ensure locale dirs & translate
    for lang in LANGUAGES:
        po_file = ensure_locale_dirs(lang)
        process_po_file(po_file, lang, cache)

    # 5) save cache
    save_cache(cache)

    # 6) compilemessages
    try:
        print("\nRunning compilemessages ...")
        run_cmd("django-admin compilemessages")
        print("Compilemessages finished.")
    except Exception as e:
        print("Error compiling messages:", e)
        print("Check .po files for header/format issues (polib saved them), then run compilemessages manually to see msgfmt output.")
        sys.exit(1)

    print("\nAll done. Restart your Django server and test languages.")

if __name__ == "__main__":
    main()
