import json
import re
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Remove all Unicode characters from the 'description' key in a JSON file"

    def handle(self, *args, **kwargs):
        input_file = "C:\\Users\\abhin\\OneDrive\\文档\\GitHub\\Hack-Babies\\myproject\\data\\nia_v1.json"
        output_file = "C:\\Users\\abhin\\OneDrive\\文档\\GitHub\\Hack-Babies\\myproject\\data\\nia_v2.json"

        try:
            # Load JSON file
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Ensure the data is a dictionary or a list
            if not isinstance(data, (list, dict)):
                raise CommandError("JSON root must be a dictionary or list")

            # Function to clean 'description' fields recursively
            def clean_descriptions(obj):
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        if key == 'description' and isinstance(value, str):
                            # Remove all Unicode characters
                            obj[key] = re.sub(r'[^\x00-\x7F]+', '', value)
                        else:
                            clean_descriptions(value)
                elif isinstance(obj, list):
                    for item in obj:
                        clean_descriptions(item)

            clean_descriptions(data)

            # Save the cleaned data
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            self.stdout.write(self.style.SUCCESS(f"Successfully removed Unicode characters from '{input_file}' and saved to '{output_file}'"))

        except FileNotFoundError:
            raise CommandError(f"File '{input_file}' does not exist.")
        except json.JSONDecodeError as e:
            raise CommandError(f"Error parsing JSON file: {e}")
