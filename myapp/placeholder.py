import polib
import re

po = polib.pofile(r"D:/Django-Ecommerce-app/myapp/myapp/locale/ta/LC_MESSAGES/django.po")
PLACEHOLDER_PATTERN = r'%\([^)]+\)s'

for entry in po:
    msgid_ph = re.findall(PLACEHOLDER_PATTERN, entry.msgid)
    msgstr_ph = re.findall(PLACEHOLDER_PATTERN, entry.msgstr)
    if msgid_ph != msgstr_ph:
        print("Mismatch!")
        print("msgid:", entry.msgid)
        print("msgstr:", entry.msgstr)
        print("Placeholders in msgid:", msgid_ph)
        print("Placeholders in msgstr:", msgstr_ph)
