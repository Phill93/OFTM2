from django.contrib import admin

from OFTM2.apps.tournament_management.models import Tournament, Combat


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'ageclass', 'participants_count']


@admin.register(Combat)
class CombatAdmin(admin.ModelAdmin):
    list_display = ['tournament', 'fighter1', 'fighter1_points', 'fighter2_points', 'fighter2']
