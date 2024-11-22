import json
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Prepend a string to the 'description' key in a JSON file"

    def handle(self, *args, **kwargs):
        # Path to your JSON file
        input_file = "C:\\Users\\abhin\\OneDrive\\文档\\GitHub\\Hack-Babies\\myproject\\data\\nia_v7.json"
        output_file = "C:\\Users\\abhin\\OneDrive\\文档\\GitHub\\Hack-Babies\\myproject\\data\\nia_v8.json"

        # Function to prepend a string to the 'description' key
        def prepend_to_description(data):
            for item in data:
                if isinstance(item, dict) and "description" in item:
                    item["description"] = "According to " + item['name'] + ", " + item["description"]
            return data

        try:
            # Open the JSON file with the correct encoding (e.g., 'utf-8')
            with open(input_file, 'r', encoding='utf-8') as file:
                json_data = json.load(file)

            # Process the data
            modified_data = prepend_to_description(json_data)

            # Save the modified data back to a JSON file
            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(modified_data, file, indent=4, ensure_ascii=False)

            self.stdout.write(self.style.SUCCESS(f"Descriptions updated and saved to {output_file}"))

        except UnicodeDecodeError as e:
            self.stderr.write(self.style.ERROR(f"Encoding error: {e}"))
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR("Input file not found."))
        except json.JSONDecodeError:
            self.stderr.write(self.style.ERROR("Invalid JSON format."))
