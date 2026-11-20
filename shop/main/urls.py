from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('registration/', views.registration, name='registration'),
    path('cards/', views.cards, name='cards'),
    path('cards/add/', views.create_card, name='create_card'),

]
