from django.db import models
from django.urls import reverse
from django.core.exceptions import FieldError

from OFTM2.apps.fencers_management.models import Fencer, AgeClass


class Tournament(models.Model):
    """Represents a tournament"""
    name = models.CharField(
        verbose_name='Name',
        max_length=60
    )
    date = models.DateField(
        verbose_name="Austragungsdatum",
        blank=True
    )
    participants = models.ManyToManyField(
        Fencer,
        verbose_name="Teilnehmer",
        blank=True
    )
    ageclass = models.ForeignKey(
        AgeClass,
        on_delete=models.CASCADE,
        verbose_name="Altersklasse"
    )

    def __str__(self):
        """Returns the name of the tournament"""
        return self.name

    def participants_count(self):
        """Returns the count of participants"""
        return self.participants.count()

    def get_absolute_url(self):
        """returns the absolute url to the object"""
        return reverse('tournament_management:tournament_detail', args=[str(self.id)])

    def new_round(self):


    participants_count.short_description = "Teilnehmeranzahl"

    class Meta:
        verbose_name = "Tunier"
        verbose_name_plural = "Turniere"


class Round(models.Model):
    """Represents a round"""
    round_number = models.IntegerField(
        verbose_name="Runde"
    )

    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        verbose_name="Tunier"
    )

    locked = models.BooleanField(
        verbose_name="Gesperrt",
        default=False
    )

    def __str__(self):
        """Returns a assembeld name"""
        return "Runde " + self.round_number.__str__() + " vom Tunier " + self.tournament.__str__()

    def save(self, *args, **kwargs):
        original = Round.objects.get(pk=self.pk)
        if original.locked:
            raise FieldError('"{}" is locked.'.format(self.__str__()))
        super(Round, self).save(*args, **kwargs)

    def get_round_before(self):
        if self.round_number <= 1:
            return None
        else:
            return self.tournament.round_set.get(round_number__exact=self.round_number-1)

    class Meta:
        verbose_name = "Runde"
        verbose_name_plural = "Runden"


class Combat(models.Model):
    """Represents a combat"""
    related_round = models.ForeignKey(
        Round,
        on_delete=models.CASCADE,
        verbose_name="Runde"
    )

    fighter1 = models.ForeignKey(
        Fencer,
        on_delete=models.CASCADE,
        verbose_name="Kämpfer 1",
        related_name="+"
    )

    fighter2 = models.ForeignKey(
        Fencer,
        on_delete=models.CASCADE,
        verbose_name="Kämpfer 2",
        related_name="+"
    )

    fighter1_points = models.IntegerField(
        verbose_name="Punkte Fechter 1"
    )

    fighter2_points = models.IntegerField(
        verbose_name="Punkte Fechter 2"
    )

    locked = models.BooleanField(
        verbose_name="Gesperrt",
        default=False
    )

    def __str__(self):
        """Returns a assembeld name"""
        return "Kampf: " + self.fighter1.__str__() + " vs " + self.fighter2.__str__() + " (" + self.related_round.__str__() + ")"

    def get_winner(self):
        """Returns the winner"""
        if self.fighter1_points > self.fighter2_points:
            return self.fighter1
        elif self.fighter1_points == self.fighter2_points:
            return None
        else:
            return self.fighter2

    def get_update_url(self):
        """returns the update url to the object"""
        return reverse('tournament_management:combat_update', args=[str(self.id)])

    def save(self, *args, **kwargs):
        original = Round.objects.get(pk=self.pk)
        if original.locked:
            raise FieldError('"{}" is locked.'.format(self.__str__()))
        super(Combat, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Kampf"
        verbose_name_plural = "Kämpfe"
