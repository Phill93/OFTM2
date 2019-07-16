from django.test import TestCase
from OFTM2.apps.fencers_management.factories import FencerItemFactory
from OFTM2.apps.tournament_management.models import Tournament, Result
from OFTM2.apps.fencers_management.models import AgeClass
import random


class TournamentEvaluationCheck(TestCase):

    def setUp(self):
        fencers = FencerItemFactory.create_batch(20)
        ag = AgeClass.objects.create(name="All", startAge=0, endAge=99)
        self.tournament = Tournament.objects.create(name="Test", date="2020-01-01", ageclass=ag)
        self.tournament.participants.set(fencers)

    def testRoundCreation(self):
        self.tournament.new_round()
        self.assertEqual(self.tournament.round_set.first().round_number, 1)

    def testRoundCombatCreation(self):
        self.tournament.new_round()
        self.tournament.round_set.get(pk=1).create_combats()
        self.assertEqual(self.tournament.round_set.get(pk=1).combat_set.count(), self.tournament.participants.count()/2)

    def testRoundCombatsEvaluation(self):
        self.tournament.new_round()
        r = self.tournament.round_set.get(pk=1)
        r.create_combats()
        for c in r.combat_set.all():
            c.fighter1_points = random.randrange(1, 5)
            c.fighter2_points = random.randrange(1, 5)
            c.save()
        r.finish()
        for c in r.combat_set.all():
            self.assertEqual(c.locked, True)
            self.assertIsInstance(c.result_set.first(), Result)
        self.assertEqual(r.locked, True)