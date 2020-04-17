from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search_word', views.search_word, name='search_word'),
    path('pop_database/', views.pop_database, name='pop_database'),
]