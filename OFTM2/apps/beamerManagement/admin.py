from django.contrib import admin
from .models import Beamer

# Register your models here.

@admin.register(Beamer)
class BeamerAdmin(admin.ModelAdmin):
    pass