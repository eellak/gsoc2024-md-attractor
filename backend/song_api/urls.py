from django.urls import path
from song_api import views

urlpatterns = [
    path('', views.trackDetails, name='home'),
    path('history/', views.searchHistory, name='history'),
]