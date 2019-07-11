'''Tournament Management URL Config'''
from django.urls import path

from . import views

app_name = 'tournament_management'

urlpatterns = [
    path('', views.TournamentsListView.as_view(), name='tournaments_list'),
    path('<int:tournament_id>', views.TournamentsDetailView.as_view(), name='tournament_detail'),
    path('add', views.TournamentCreateView.as_view(), name='tournament_create'),
    path('<int:pk>/update', views.TournamentUpdateView.as_view(), name='tournament_update'),
    path('<int:pk>/delete', views.TournamentDeleteView.as_view(), name='tournament_delete'),
    path('combat/<int:pk>/update', views.CombatUpdateView.as_view(), name='combat_update'),
]
