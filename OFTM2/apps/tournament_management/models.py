from django.db import models
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

    participants_count.short_description = "Teilnehmeranzahl"

    class Meta:
        verbose_name = "Tunier"
        verbose_name_plural = "Turniere"
