'''Fencers Management URL Config'''
from django.urls import path
from . import views

app_name = 'fencers_management'

urlpatterns = [
    path('', views.FencersListView.as_view(), name='fencers_list'),
    path('<int:fencer_id>', views.FencersDetailView.as_view(), name='fencer_detail')
]
