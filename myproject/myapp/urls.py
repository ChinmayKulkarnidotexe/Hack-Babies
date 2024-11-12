from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    #path('counter', views.counter, name='counter')
    path('search-page', views.search_page, name='search-page')
    #path('counter', views.counter, name='counter')
    #path('counter', views.counter, name='counter')
    #path('counter', views.counter, name='counter')
    #path('counter', views.counter, name='counter')
    #path('counter', views.counter, name='counter')
]
