"""menus for fencers management app"""
from menu import Menu, MenuItem
from django.urls import reverse

Menu.add_item("main", MenuItem("Fechter/innen", reverse('fencers_management:fencers_list')))
#Menu.add_item("user", MenuItem("Profil", reverse('profile')))
Menu.add_item("user", MenuItem("Logout", reverse('logout')))