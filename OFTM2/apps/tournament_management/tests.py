from django.test import TestCase
from OFTM2.apps.fencers_management.factories import FencerItemFactory
from OFTM2.apps.tournament_management.models import Tournament, Result, Round, Combat
from OFTM2.apps.fencers_management.models import AgeClass, Fencer
import random
import json
import os
from django.conf import settings


class TournamentEvaluationCheck(TestCase):

    def setUp(self):
        fencers = FencerItemFactory.create_batch(20)
        ag = AgeClass.objects.create(name="All", startAge=0, endAge=99)
        self.tournament = Tournament.objects.create(name="Test", date="2020-01-01", ageclass=ag)
        self.tournament.participants.set(fencers)

    def testRoundCreation(self):
        r = self.tournament.new_round()
        self.assertEqual(r.round_number, 1)

    def testRoundCombatCreation(self):
        r = self.tournament.new_round()
        self.assertEqual(r.combat_set.count(), self.tournament.participants.count()/2)


class TournamentCalculationCheck(TestCase):
    def setUp(self):
        self.fencers = FencerItemFactory.create_batch(20)
        self.test_data = {}
        for file in os.listdir(os.path.join(settings.BASE_DIR, "apps", "tournament_management", "dummy_data", "rounds")):
            self.test_data[file] = json.loads(open(os.path.join(settings.BASE_DIR, "apps", "tournament_management", "dummy_data", "rounds" , file)).read())
        ac = AgeClass.objects.create(name="All", startAge=0, endAge=99)
        self.tournament = Tournament.objects.create(name="Test123", date="2019-12-24", ageclass=ac)
        self.tournament.participants.set(self.fencers)

    def testCalculation(self):
        self.round1()
        self.round2()

    def round1(self):
        r = Round.objects.create(round_number=1, tournament=self.tournament, locked=True)
        for td_c in self.test_data['round1.json']:
            Combat.objects.create(related_round=r, fighter1=Fencer.objects.get(pk=td_c['id1']), fighter2=Fencer.objects.get(pk=td_c['Id2']), fighter1_points=td_c['points1'], fighter2_points=td_c['points2'])
        r.finish()
        ranking = r.ranking()
        for td_r in self.test_data['round1_result.json']:
            rank = int(td_r['rank'] - 1)
            self.assertEqual(ranking[rank].fencer, Fencer.objects.get(pk=td_r['id']))
            self.assertEqual(ranking[rank].given, td_r['geg'])
            self.assertEqual(ranking[rank].recieved, td_r['recv'])
            self.assertEqual(ranking[rank].index, td_r['index'])

    def round2(self):
        r = self.tournament.new_round()
        for td_c in self.test_data['round2.json']:
            c = Combat.objects.get(fighter1_id=td_c['id1'], fighter2_id=td_c['Id2'], related_round=r)
            c.fighter1_points = td_c['points1']
            c.fighter2_points = td_c['points2']
            c.save()
        r.finish()
        ranking = r.ranking()
        for td_r in self.test_data['round2_result.json']:
            rank = int(td_r['rank'] - 1)
            self.assertEqual(ranking[rank].fencer, Fencer.objects.get(pk=td_r['id']))
            self.assertEqual(ranking[rank].given, td_r['geg'])
            self.assertEqual(ranking[rank].recieved, td_r['recv'])
            self.assertEqual(ranking[rank].index, td_r['index'])