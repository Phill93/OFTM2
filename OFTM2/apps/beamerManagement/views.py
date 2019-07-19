from django.shortcuts import render
from OFTM2.apps.beamerManagement.models import Beamer
from django.http import HttpResponse
from datetime import datetime


# Create your views here.


def beamer(request):
    if request.GET.get('id'):
        b, c = Beamer.objects.get_or_create(name=request.GET.get('id'), defaults={'last_reload': datetime.now()})
        if not c:
            b.last_reload = datetime.now()
            b.save()
        if b.tournament:
            if b.view == b.VIEW_COMBATS:
                return render(request, 'beamer.html', context={
                    'mode': "combats",
                    'beamer': b,
                    'tournament': b.tournament,
                    'combats': b.tournament.round_set.last().combat_set.all(),
                    'round': b.tournament.round_set.last()
                })
            elif b.view == b.VIEW_POINTS:
                return render(request, 'beamer.html', context={
                    'mode': "points",
                    'beamer': b,
                    'tournament': b.tournament,
                    'points': b.tournament.round_set.get(
                        round_number=b.tournament.round_set.last().round_number - 1,
                        tournament=b.tournament).ranking(),
                    'round': b.tournament.round_set.get(
                        round_number=b.tournament.round_set.last().round_number - 1,
                        tournament=b.tournament)
                })
            elif b.view == b.VIEW_BOTH:
                return render(request, 'beamer.html', context={
                    'mode': "both",
                    'beamer': b,
                    'tournament': b.tournament,
                    'points': b.tournament.round_set.get(
                        round_number=b.tournament.round_set.last().round_number - 1,
                        tournament=b.tournament).ranking(),
                    'round': b.tournament.round_set.get(
                        round_number=b.tournament.round_set.last().round_number - 1,
                        tournament=b.tournament),
                    'combats': b.tournament.round_set.last().combat_set.all()
                })
    return HttpResponse('empty')


def beamer_refresh(request):
    if request.GET.get('id'):
        b = Beamer.objects.get(name=request.GET.get('id'))
        if b.tournament:
            if b.view == b.VIEW_COMBATS:
                pass
            elif b.view == b.VIEW_POINTS:
                pass
            elif b.view == b.VIEW_BOTH:
                pass
