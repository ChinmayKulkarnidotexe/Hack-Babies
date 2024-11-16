from django.shortcuts import render
from django.conf import settings
from .models import Laws
import json
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def search(request):
    if request.method == "POST":
        raw_searched = request.POST['searched']
        searched_values = raw_searched.split()
        for searched in searched_values:
            laws = Laws.objects.filter(desc__contains=searched) | Laws.objects.filter(title__contains=searched) | Laws.objects.filter(law_name__contains=searched)
        return render(request, 'search.html', {'searched': searched,'laws':laws,'raw_searched': raw_searched})
    else:
         return render(request, 'search.html')


