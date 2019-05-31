"""view for the fencers management app"""
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views import View
from django_tables2 import RequestConfig
from django.contrib.auth.mixins import PermissionRequiredMixin

from OFTM2.apps.fencers_management.models import Fencer
from OFTM2.apps.fencers_management.tables import FencersTable
from OFTM2.apps.fencers_management.forms import FencerForm


class FencersListView(PermissionRequiredMixin, View):
    permission_required = 'Fencers.can_view'
    """show all fencers as a table"""
    def get(self, request):
        """HTTP-GET"""
        table = FencersTable(Fencer.objects.all())
        RequestConfig(request).configure(table)
        return render(request, 'fencers_list.html', {'table': table, 'title': "Liste der Fechter/innen"})


class FencersDetailView(PermissionRequiredMixin, View):
    permission_required = 'Fencers.can_view'
    """show one fencer"""
    def get(self, request, fencer_id):
        """HTTP-GET"""
        fencer = get_object_or_404(Fencer, pk=fencer_id)
        return render(request, 'fencer_detail.html', {'fencer': fencer, 'back': True, 'title': fencer})


class FencersCreateView(PermissionRequiredMixin, View):
    permission_required = 'Fencers.can_create'
    """create a new fencer"""
    def get(self, request):
        """HTTP-GET"""
        form = FencerForm()
        print(vars(form.fields['birthday']))
        return render(request, 'fencer_create.html', {'form': form, 'back': True, 'title': "Fecheter/in anlegen"})