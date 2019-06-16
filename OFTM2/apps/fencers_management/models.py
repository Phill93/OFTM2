"""Models for fencers management app"""
from django.db import models
from django.urls import reverse
from OFTM2.apps.fencers_management.validators import validate_fechtpass
from OFTM2.apps.fencers_management.helpers import calculate_age
from partial_date import PartialDateField

# Create your models here.


class Fencer(models.Model):
    """fencer model represents a fencer"""
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_CHOICES = [
        (GENDER_MALE, 'Männlich'),
        (GENDER_FEMALE, 'Weiblich')
    ]

    first_name = models.CharField(
        verbose_name='Vorname',
        max_length=60
    )
    last_name = models.CharField(
        verbose_name='Nachname',
        max_length=60
    )
    gender = models.IntegerField(
        verbose_name='Geschlecht',
        choices=GENDER_CHOICES
    )
    fechtpass = models.CharField(
        verbose_name='Fechtpass Nummer',
        blank=True,
        validators=[
            validate_fechtpass,
        ],
        max_length=9,
        unique=True,
    )
    birthday = models.DateField(
        verbose_name='Geburtsdatum'
    )

    def __str__(self):
        """returns the first and the last name"""
        return '{} {}'.format(self.first_name, self.last_name)

    def get_absolute_url(self):
        """returns the absolute url to the object"""
        return reverse('fencers_management:fencer_detail', args=[str(self.id)])

    def get_ageclasses(self):
        """returns the ageclasses for the fencer"""
        out = []
        age = calculate_age(self.birthday)
        for ageclass in AgeClass.objects.all():
            if ageclass.startAge <= age <= ageclass.endAge:
                out.append(ageclass)
        return out

    def get_age(self):
        """returns the age of a fencer"""
        return calculate_age(self.birthday)

    class Meta:
        verbose_name = "Fechter/in"
        verbose_name_plural = "Fechter/innen"


class AgeClass(models.Model):
    """represents a ageclass (see https://de.wikipedia.org/wiki/Fechten#Altersklassen)"""
    name = models.CharField(
        verbose_name="Name",
        max_length=60
    )
    startAge = models.IntegerField(
        verbose_name="Anfangs Alter",
    )
    endAge = models.IntegerField(
        verbose_name="End Alter"
    )

    def __str__(self):
        """returns the name"""
        return self.name

    class Meta:
        verbose_name = "Altersklasse"
        verbose_name_plural = "Altersklassen"