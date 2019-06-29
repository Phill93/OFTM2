"""menus for fencers management app"""
from django.urls import reverse
from menu import Menu, MenuItem

Menu.add_item("main", MenuItem("Tuniere", reverse('tournament_management:tournaments_list')))
