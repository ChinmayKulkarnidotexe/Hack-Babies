import json
import os
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Combine all JSON files in a folder into a single JSON file"
    
    def handle(self, *args, **kwargs):
        input_folder = 'C:\\Users\\abhin\\OneDrive\\文档\\GitHub\\Hack-Babies\\myproject\\data\\combine'
        output_file = 'C:\\Users\\abhin\\OneDrive\\文档\\GitHub\\Hack-Babies\\myproject\\data\\final_database_v1.json'
        combined_data = []

        try:
            # Ensure the folder exists
            if not os.path.isdir(input_folder):
                self.stderr.write(self.style.ERROR(f"The directory '{input_folder}' does not exist."))
                return

            # Loop through all files in the directory
            for filename in os.listdir(input_folder):
                file_path = os.path.join(input_folder, filename)

                # Only process .json files
                if filename.endswith('.json'):
                    self.stdout.write(f"Processing file: {filename}")
                    try:
                        with open(file_path, 'r', encoding='utf-8') as file:
                            data = json.load(file)

                            # Ensure the data is a list or dictionary
                            if isinstance(data, list):
                                combined_data.extend(data)  # Add list items to the combined data
                            elif isinstance(data, dict):
                                combined_data.append(data)  # Add dictionary as a single item
                            else:
                                self.stderr.write(self.style.WARNING(f"Skipping unsupported format in {filename}."))
                    except json.JSONDecodeError as e:
                        self.stderr.write(self.style.ERROR(f"Error parsing JSON file '{filename}': {e}"))
                    except UnicodeDecodeError as e:
                        self.stderr.write(self.style.ERROR(f"Encoding error in file '{filename}': {e}"))

            # Save the combined data to the output file
            with open(output_file, 'w', encoding='utf-8') as output_file:
                json.dump(combined_data, output_file, indent=4, ensure_ascii=False)

            self.stdout.write(self.style.SUCCESS(f"Successfully combined files into '{output_file.name}'"))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred: {e}"))
