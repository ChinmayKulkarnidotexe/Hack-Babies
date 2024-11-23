import json
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Replace 'article' key with 'name' key in a JSON file"

    def handle(self, *args, **kwargs):
        # Path to your JSON file
        input_file = "C:\\Users\\abhin\\OneDrive\\文档\\GitHub\\Hack-Babies\\myproject\\data\\final_clean_constitution.json"
        output_file= "C:\\Users\\abhin\\OneDrive\\文档\\GitHub\\Hack-Babies\\myproject\\data\\final_clean_constitution_v2.json"

        # Function to replace 'section' with 'name'
        def replace_key(data):
            if isinstance(data, dict):
                return {
                    ('name' if k == 'article' else k): replace_key(v)
                    for k, v in data.items()
                }
            elif isinstance(data, list):
                return [replace_key(item) for item in data]
            else:
                return data

        try:
            # Open the JSON file with the correct encoding (e.g., 'utf-8')
            with open(input_file, 'r', encoding='utf-8') as file:
                json_data = json.load(file)

            # Process the data
            modified_data = replace_key(json_data)

            # Save the modified data back to a JSON file
            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(modified_data, file, indent=4)

            self.stdout.write(self.style.SUCCESS(f"'article' key replaced with 'name' and saved to {output_file}"))

        except UnicodeDecodeError as e:
            self.stderr.write(self.style.ERROR(f"Encoding error: {e}"))
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR("Input file not found."))
        except json.JSONDecodeError:
            self.stderr.write(self.style.ERROR("Invalid JSON format."))
