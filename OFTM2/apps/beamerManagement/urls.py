'''Fencers Management URL Config'''
from django.urls import path
from . import views

app_name = 'beamer_management'

urlpatterns = [
    path('', views.beamer, name='beamer'),
]
