import os
import polib
from deep_translator import GoogleTranslator
import time
import re

# --------------------------
# Configuration
# --------------------------

# Path to your Django locale folder
LOCALE_DIR = os.path.join(os.path.dirname(__file__), 'myapp', 'locale')

# Target languages (must match the folder names in locale/)
LANGUAGES = ['hi', 'te', 'ta']  # Hindi, Telugu, Tamil

# Delay between translations to avoid rate limits
DELAY_BETWEEN_TRANSLATIONS = 0.3  # seconds

# --------------------------
# Functions
# --------------------------

def preserve_placeholders(text):
    """
    Extract placeholders like %(var)s and replace them with temporary tags for translation.
    After translation, restore the original placeholders.
    """
    placeholders = re.findall(r'%\([^)]+\)s', text)
    temp_text = text
    mapping = {}

    for i, ph in enumerate(placeholders):
        key = f"__PH_{i}__"
        mapping[key] = ph
        temp_text = temp_text.replace(ph, key)

    return temp_text, mapping

def restore_placeholders(translated_text, mapping):
    for key, ph in mapping.items():
        translated_text = translated_text.replace(key, ph)
    return translated_text

def auto_translate_po(lang_code):
    po_path = os.path.join(LOCALE_DIR, lang_code, 'LC_MESSAGES', 'django.po')
    print(f"\nLooking for {po_path}")

    if not os.path.exists(po_path):
        print(f"No .po file found for language '{lang_code}'")
        return

    po = polib.pofile(po_path)
    updated = False

    for entry in po:
        # Skip entries that are already translated
        if entry.msgstr.strip() and entry.msgstr.strip() != entry.msgid.strip():
            continue
        if not entry.msgid.strip():
            continue

        try:
            # Preserve placeholders before translation
            temp_text, mapping = preserve_placeholders(entry.msgid)

            # Translate
            translation = GoogleTranslator(source='auto', target=lang_code).translate(temp_text)

            # Restore placeholders after translation
            translation = restore_placeholders(translation, mapping)

            entry.msgstr = translation
            updated = True
            print(f"Translated: '{entry.msgid}' → '{translation}'")
            time.sleep(DELAY_BETWEEN_TRANSLATIONS)  # avoid rate limits
        except Exception as e:
            print(f"Error translating '{entry.msgid}': {e}")

    if updated:
        po.save()
        print(f"✅ Updated translations saved for '{lang_code}'")
    else:
        print(f"No untranslated strings found for '{lang_code}'")

# --------------------------
# Main
# --------------------------

if __name__ == "__main__":
    for lang in LANGUAGES:
        auto_translate_po(lang)
        print("="*60)
