from factory_djoy import CleanModelFactory
from factory.fuzzy import FuzzyText, FuzzyInteger, FuzzyDate
import factory
from OFTM2.apps.fencers_management.models import Fencer
import datetime
import random


class FencerItemFactory(CleanModelFactory):
    class Meta:
        model = Fencer

    first_name = factory.Faker('first_name', locale='de_DE')
    last_name = factory.Faker('last_name', locale='de_DE')
    gender = FuzzyInteger(0, 1)
    birthday = FuzzyDate(datetime.date(1900, 1, 1), datetime.date.today())
    fechtpass = factory.LazyFunction(lambda: "GER{:06d}".format(random.randint(0, 999999)))
