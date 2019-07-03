from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_tables2 import RequestConfig

from OFTM2.apps.fencers_management.helpers import calculate_birthday
from OFTM2.apps.fencers_management.models import Fencer
from OFTM2.apps.fencers_management.tables import FencersTable
from OFTM2.apps.tournament_management.forms import TournamentForm
from OFTM2.apps.tournament_management.models import Tournament
from OFTM2.apps.tournament_management.tables import TournamentTable


class TournamentsListView(PermissionRequiredMixin, View):
    permission_required = 'Tournament.can_view'
    """show all tournaments as a table"""

    def get(self, request):
        """HTTP-GET"""
        table = TournamentTable(Tournament.objects.all())
        RequestConfig(request).configure(table)
        return render(request, 'tournaments_list.html', {'table': table, 'title': "Liste der Tuniere"})


class TournamentsDetailView(PermissionRequiredMixin, View):
    permission_required = 'Tournament.can_view'
    """show one tournament"""

    def get(self, request, tournament_id):
        """HTTP-GET"""
        tournament = get_object_or_404(Tournament, pk=tournament_id)
        participants_table = FencersTable(tournament.participants.all())
        return render(request, 'tournament_detail.html', {'tournament': tournament, 'participants_table': participants_table, 'back': True, 'title': tournament})


class TournamentCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'Tournament.can_create'
    """create a new tournament"""
    form_class = TournamentForm
    template_name = 'tournament_form.html'
    model = Tournament


class TournamentUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'Tournament.can_edit'
    """update a tournament"""
    form_class = TournamentForm
    template_name = 'tournament_form.html'
    model = Tournament

    def dispatch(self, request, *args, **kwargs):
        t = Tournament.objects.get(pk=kwargs['pk'])
        ac = t.ageclass
        self.form_class.base_fields['participants'].queryset = Fencer.objects.filter(
            birthday__range=[calculate_birthday(t.date, ac.endAge), calculate_birthday(t.date, ac.startAge)])
        return super(TournamentUpdateView, self).dispatch(request, *args, **kwargs)


class TournamentDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'Tournament.can_delete'
    """delete a tournament"""
    form_class = TournamentForm
    template_name = 'tournament_delete.html'
    model = Tournament
    success_url = reverse_lazy('tournament_management:tournaments_list')
