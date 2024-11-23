import json
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Remove a specific key from a JSON file"

    def handle(self, *args, **kwargs):
        # Path to your JSON file
        input_file = "C:\\Users\\arjun\\Downloads\\Indian-Law-Penal-Code-Json-main\\Indian-Law-Penal-Code-Json-main\\edit 4 files\\iea.json"
        output_file = "C:\\Users\\arjun\\OneDrive\\Documents\\GitHub\\Hack-Babies\\myproject\\iea_2.json"

        # Key to remove
        key_to_remove = "chapter"  # Replace this with the desired key

        # Function to remove the specified key
        def remove_key(data):
            if isinstance(data, dict):
                return {k: remove_key(v) for k, v in data.items() if k != key_to_remove}
            elif isinstance(data, list):
                return [remove_key(item) for item in data]
            else:
                return data

        try:
            # Open the JSON file with the correct encoding (e.g., 'utf-8')
            with open(input_file, 'r', encoding='utf-8') as file:
                json_data = json.load(file)

            # Process the data
            modified_data = remove_key(json_data)

            # Save the modified data back to a JSON file
            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(modified_data, file, indent=4)

            self.stdout.write(self.style.SUCCESS(f"Key '{key_to_remove}' removed and saved to {output_file}"))

        except UnicodeDecodeError as e:
            self.stderr.write(self.style.ERROR(f"Encoding error: {e}"))
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR("Input file not found."))
        except json.JSONDecodeError:
            self.stderr.write(self.style.ERROR("Invalid JSON format."))
