from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    content = {
        'name': 'Abhinav',
        'age': '18'
    }
    return render(request, 'index.html', content)

# def counter(request):
#     text = request.POST['text']
#     amount_of_words = len(text.split())
#     return render(request, 'counter.html', {'amount': amount_of_words})

def search_page(request):
    return render(request, 'search-page.html')