import os
import subprocess
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = "Auto-extract, clean, and compile translations for all languages."

    def handle(self, *args, **kwargs):
        # List of languages you want
        languages = ['ta', 'te', 'kn', 'hi']

        locale_path = os.path.join(settings.BASE_DIR, 'myapp', 'locale')

        # Step 1: Remove old .mo files to avoid conflicts
        self.stdout.write("Cleaning old .mo files...")
        for root, dirs, files in os.walk(locale_path):
            for file in files:
                if file.endswith('.mo') or file.endswith('.po'):
                    os.remove(os.path.join(root, file))

        # Step 2: Generate .po files for each language
        self.stdout.write("Extracting messages for all languages...")
        for lang in languages:
            self.stdout.write(f"  Generating messages for {lang}...")
            subprocess.run(
                ['django-admin', 'makemessages', '-l', lang],
                check=True
            )

        # Step 3: Compile messages into .mo
        self.stdout.write("Compiling translations...")
        subprocess.run(
            ['django-admin', 'compilemessages'],
            check=True
        )

        self.stdout.write(self.style.SUCCESS("✅ All translations extracted and compiled successfully!"))
