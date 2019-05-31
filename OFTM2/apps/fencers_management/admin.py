"""Django admin configuration for fencers management"""
from django.contrib import admin
from .models import Fencer, AgeClass


@admin.register(Fencer)
class FencerAdmin(admin.ModelAdmin):
    """
    Register a admin page for the fencer model
    """
    list_display = (
        'first_name',
        'last_name',
        'birthday',
        'fechtpass'
    )

@admin.register(AgeClass)
class AgeClassAdmin(admin.ModelAdmin):
    """
    Register a admin page for the AgeClass model
    """
    list_display = (
        'name',
        'startDate',
        'endDate'
    )