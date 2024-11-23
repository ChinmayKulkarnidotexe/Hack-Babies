import json
import re
from django.core.management.base import BaseCommand

def add_new_key_to_json(input_file, output_file, new_key, source_key):
    """
    Adds a new key to each object in the JSON file, copying values from the source key.
    """
    # Load the JSON data
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Add the new key to each item
    for item in data:
        if source_key in item:  # Check if the source key exists
            item[new_key] = item[source_key]
        else:
            item[new_key] = None  # Add the new key with a default value if source key is missing

    # Write the updated data back to a new file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)




class Command(BaseCommand):
    help = 'Create a new key called info'

    def handle(self, *args, **options):
        try:
            input_file = 'C:\\Users\\abhin\\OneDrive\\文档\\GitHub\\Hack-Babies\\myproject\\data\\nia_v5.json'  # Replace with your input file path
            output_file = 'C:\\Users\\abhin\\OneDrive\\文档\\GitHub\\Hack-Babies\\myproject\\data\\nia_v6.json'  # Replace with your desired output file path
            new_key = 'info'  # Name of the new key to add
            source_key = 'description'  # Existing key from which to copy values

            add_new_key_to_json(input_file, output_file, new_key, source_key)
            
            # Write the cleaned data to a new file
            self.stdout.write(self.style.SUCCESS(f"Created a new key and JSON saved to: {output_file}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred: {e}"))
