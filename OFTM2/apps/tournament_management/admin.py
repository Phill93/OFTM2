from django.contrib import admin

from OFTM2.apps.tournament_management.models import Tournament, Combat, Round


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'ageclass', 'participants_count']


@admin.register(Combat)
class CombatAdmin(admin.ModelAdmin):
    list_display = ['related_round', 'fighter1', 'fighter1_points', 'fighter2_points', 'fighter2']


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ['round_number', 'tournament']