from django.db import models
from django.urls import reverse

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

    participants_count.short_description = "Teilnehmeranzahl"

    class Meta:
        verbose_name = "Tunier"
        verbose_name_plural = "Turniere"


class Combat(models.Model):
    """Represents a combat"""
    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.CASCADE,
        verbose_name="Tunier"
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

    def __str__(self):
        """Returns a assembeld name"""
        return "Kampf: " + self.fighter1.__str__() + " vs " + self.fighter2.__str__() + " (Tunier " + self.tournament.__str__() + ")"

    def get_winner(self):
        """Returns the winner"""
        if self.fighter1_points > self.fighter2_points:
            return self.fighter1
        elif self.fighter1_points == self.fighter2_points:
            return None
        else:
            return self.fighter2

    class Meta:
        verbose_name = "Kampf"
        verbose_name_plural = "Kämpfe"
