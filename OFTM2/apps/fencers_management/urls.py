'''Fencers Management URL Config'''
from django.urls import path
from . import views

app_name = 'fencers_management'

urlpatterns = [
    path('', views.FencersListView.as_view(), name='fencers_list'),
    path('<int:fencer_id>', views.FencersDetailView.as_view(), name='fencer_detail'),
    path('add', views.FencersCreateView.as_view(), name='fencer_create'),
    path('<int:pk>/update', views.FencersUpdateView.as_view(), name='fencer_update')
]
