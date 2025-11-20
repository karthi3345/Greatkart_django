import polib
from pathlib import Path
import re
import subprocess

PROJECT_ROOT = Path.cwd()
LOCALE_DIR = PROJECT_ROOT / "locale"

HEADER_TEMPLATE = {
    "Project-Id-Version": "1.0",
    "Report-Msgid-Bugs-To": "",
    "POT-Creation-Date": "",
    "PO-Revision-Date": "",
    "Last-Translator": "",
    "Language-Team": "",
    "Language": "",
    "MIME-Version": "1.0",
    "Content-Type": "text/plain; charset=UTF-8",
    "Content-Transfer-Encoding": "8bit",
}

def fix_header(po: polib.POFile, lang: str):
    """Ensure header exists and charset is set."""
    if not po.metadata:
        po.metadata = {}

    for key, default_value in HEADER_TEMPLATE.items():
        if key == "Language":
            po.metadata[key] = lang
        elif key not in po.metadata:
            po.metadata[key] = default_value
        elif key == "Content-Type":
            if "charset" not in po.metadata[key]:
                po.metadata[key] = "text/plain; charset=UTF-8"


def fix_multiline_breaks(po: polib.POFile):
    """Fix entries where msgid/msgstr formatting is corrupted."""
    for entry in po:
        # Remove blank-line-only msgid/msgstr
        if entry.msgid is None:
            entry.msgid = ""
        if entry.msgstr is None:
            entry.msgstr = ""

        # Fix entries that start incorrectly
        if entry.msgid.startswith("\n") and not entry.msgstr.startswith("\n"):
            entry.msgstr = "\n" + entry.msgstr

        if entry.msgstr.startswith("\n") and not entry.msgid.startswith("\n"):
            entry.msgid = "\n" + entry.msgid


def process_po_file(po_path: Path, lang: str):
    print(f"\nFixing {po_path}")

    po = polib.pofile(str(po_path))

    # Fix header
    fix_header(po, lang)

    # Fix multiline issues
    fix_multiline_breaks(po)

    # Save back
    po.save(str(po_path))
    print(f"✔ Saved fixed file: {po_path}")


def main():
    print("Searching for .po files...\n")

    for lang_dir in LOCALE_DIR.iterdir():
        lang = lang_dir.name

        po_path = lang_dir / "LC_MESSAGES" / "django.po"
        if po_path.exists():
            process_po_file(po_path, lang)

    print("\nRunning compilemessages...")
    try:
        subprocess.run("django-admin compilemessages", shell=True, check=True)
        print("\n✔ All languages compiled successfully!")
    except Exception as e:
        print("\n❌ Still errors exist! Check output above.")
        print(e)


if __name__ == "__main__":
    main()
