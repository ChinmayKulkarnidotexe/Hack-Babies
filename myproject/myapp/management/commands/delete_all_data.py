from django.core.management.base import BaseCommand
from myapp.models import Laws

class Command(BaseCommand):
    help = 'Delete all data from Laws model'

    def handle(self, *args, **kwargs):
        
        Laws.objects.all().delete()
        
        self.stdout.write(self.style.SUCCESS('Successfully deleted all data from Laws model'))