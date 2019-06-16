from django.contrib import admin
from OFTM2.apps.tournament_management.models import Tournament


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'ageclass', 'participants_count']