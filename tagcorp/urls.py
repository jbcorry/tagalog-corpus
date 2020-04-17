from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search_word', views.search_word, name='search_word'),
    path('pop_database/', views.pop_database, name='pop_database'),
    path('signin', views.signIn, name='signin'),
    path('postsign/', views.postsign, name='signin'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signUp, name='signup'),
    path('postsignup/', views.postsignup, name='postsignup'),
    path('create/', views.create, name='create'),
    path('postcreate/', views.postcreate, name='postcreate'),
    path('check/', views.check, name='check'),
]