import json
import re
from django.core.management.base import BaseCommand

def clean_text(text):
    """
    Cleans input text by:
    - Removing HTML tags (e.g., <br>)
    - Removing bullet points (e.g., (1), (2), •)
    - Removing special symbols
    - Normalizing spaces
    """
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Remove bullet points like (1), (2)
    text = re.sub(r'\(\d+\)', ' ', text)
    # Remove special bullet points like •, *, -, etc.
    text = re.sub(r'[\u2022•*–-]', ' ', text)
    # Remove any extra special characters (you can expand this as needed)
    text = re.sub(r'[^\w\s.,]', ' ', text)
    # Normalize multiple spaces to a single space
    text = re.sub(r'\s+', ' ', text).strip()
    return text

class Command(BaseCommand):
    help = 'Cleans the JSON data file by removing HTML tags, bullet points, and special symbols.'

    def handle(self, *args, **options):
        input_file = 'updated_constitution.json'
        output_file = 'cleaned_updated_constitution.json'

        try:
            # Load the JSON data
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Clean the text in 'title' and 'description' fields
            cleaned_data = []
            for item in data:
                cleaned_item = {
                    "article": item.get("article", ""),  # Preserve the article field as-is
                    "title": clean_text(item.get("title", "")),  # Clean the title
                    "description": clean_text(item.get("description", "")),  # Clean the description
                    "info": item.get("info", "")  # New info key
                }
                cleaned_data.append(cleaned_item)
            
            # Write the cleaned data to a new file
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(cleaned_data, f, ensure_ascii=False, indent=4)
            self.stdout.write(self.style.SUCCESS(f"Cleaned JSON saved to: {output_file}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred: {e}"))
