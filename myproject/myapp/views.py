from django.shortcuts import render
from django.conf import settings
from .models import Laws

# Create your views here.
def index(request):
    return render(request, 'index.html')

# def search(request):
#     query = request.POST.get('search')
#     #print("Search Query:", query)
#     return render(request, 'search.html',{'query': query})

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        laws = Laws.objects.filter(name__contains=searched)
        return render(request, 'search.html', {'searched': searched,'laws':laws})
    else:
         return render(request, 'search.html')

