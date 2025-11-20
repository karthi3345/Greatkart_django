import polib
import re
import os

PLACEHOLDER_PATTERN = r'%\([^)]+\)s'

def fix_placeholders(entry):
    # Find placeholders in msgid
    msgid_placeholders = re.findall(PLACEHOLDER_PATTERN, entry.msgid)
    if not msgid_placeholders:
        return
    
    # Map placeholder names
    placeholder_map = {
        re.match(r'%\(([^)]+)\)s', ph).group(1): ph
        for ph in msgid_placeholders
    }

    # Fix msgstr by matching same names
    def replace(match):
        name = re.match(r'%\(([^)]+)\)s', match.group(0)).group(1)
        return placeholder_map.get(name, match.group(0))

    if entry.msgstr:
        entry.msgstr = re.sub(PLACEHOLDER_PATTERN, replace, entry.msgstr)

def fix_po_file(po_file_path):
    print(f"Processing: {po_file_path}")
    po = polib.pofile(po_file_path)
    for entry in po:
        fix_placeholders(entry)
    po.save(po_file_path)
    print(f"✔ Fixed: {po_file_path}")

# ---- CONFIG ----
base_dir = r"D:/Django-Ecommerce-app/myapp/myapp/locale"
languages = ['ta', 'hi', 'te', 'kn']

# ---- EXECUTE ----
for lang in languages:
    po_path = os.path.join(base_dir, lang, "LC_MESSAGES", "django.po")
    if os.path.exists(po_path):
        fix_po_file(po_path)
    else:
        print(f"✖ File not found: {po_path}")
