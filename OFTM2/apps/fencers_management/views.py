"""view for the fencers management app"""
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views import View
from django_tables2 import RequestConfig

from OFTM2.apps.fencers_management.models import Fencer
from OFTM2.apps.fencers_management.tables import FencersTable


class FencersListView(View):
    """show all fencers as a table"""
    def get(self, request):
        """HTTP-GET"""
        table = FencersTable(Fencer.objects.all())
        RequestConfig(request).configure(table)
        return render(request, 'fencers_list.html', {'table': table, 'title': "Liste der Fechter/innen"})


class FencersDetailView(View):
    """show one fencer"""
    def get(self, request, fencer_id):
        """HTTP-GET"""
        fencer = get_object_or_404(Fencer, pk=fencer_id)
        return render(request, 'fencer_detail.html', {'fencer': fencer, 'back': True, 'title': fencer})
