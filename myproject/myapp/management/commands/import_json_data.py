import json
from django.core.management.base import BaseCommand
from myapp.models import Laws

class Command(BaseCommand):
    help = 'Load data from JSON file into Laws model'

    def handle(self, *args, **kwargs):
        
        with open('constitution_of_india.json', 'r',encoding='utf-8') as file:
            data = json.load(file)
            # ['ConstitutionOfIndia']['Parts']
            
        # part_names = ['Part I','Part II','Part III','Part IV','Part IVA','Part V']
        
        # articles = {"Part I":[
        #         "Article 1",
        #         "Article 2",
        #         "Article 3",
        #         "Article 4"],
        #     "Part II": [
        #         "Article 5",
        #         "Article 6",
        #         "Article 7",
        #         "Article 8",
        #         "Article 9",
        #         "Article 10",
        #         "Article 11"],
        #     "Part III": [
        #         "Article 12",
        #         "Article 13",
        #         "Article 14",
        #         "Article 15",
        #         "Article 16",
        #         "Article 17",
        #         "Article 18",
        #         "Article 19",
        #         "Article 20",
        #         "Article 21",
        #         "Article 22",
        #         "Article 23",
        #         "Article 24",
        #         "Article 25",
        #         "Article 26",
        #         "Article 27",
        #         "Article 28",
        #         "Article 29",
        #         "Article 30",
        #         "Article 31",
        #         "Article 32",
        #         "Article 33",
        #         "Article 34",
        #         "Article 35"],
        #     "Part IV": [
        #         "Article 36",
        #         "Article 37",
        #         "Article 38",
        #         "Article 39",
        #         "Article 40",
        #         "Article 41",
        #         "Article 42",
        #         "Article 43",
        #         "Article 44",
        #         "Article 45",
        #         "Article 46",
        #         "Article 47",
        #         "Article 48",
        #         "Article 49",
        #         "Article 50",
        #         "Article 51"],
        #     "Part IVA":
        #         ["Article 51A"],
        #     "Part V": [
        #         "Article 52",
        #         "Article 53",
        #         "Article 54",
        #         "Article 55",
        #         "Article 56",
        #         "Article 57",
        #         "Article 58",
        #         "Article 59",
        #         "Article 60",
        #         "Article 61",
        #         "Article 62",
        #         "Article 63",
        #         "Article 64",
        #         "Article 65",
        #         "Article 66",
        #         "Article 67",
        #         "Article 68",
        #         "Article 69",
        #         "Article 70"]
        #     }
        
        # for part in part_names:
        #     for article in articles[part]:

        #         Laws.objects.create(law_name=article,title=data[part]['Articles'][article]['Title'], text=data[part]['Articles'][article]['Text'])

        for item in data:
            Laws.objects.create(law_name=item['article'], title=item['title'], desc=item['description'])

        self.stdout.write(self.style.SUCCESS('Successfully imported data into Laws model'))