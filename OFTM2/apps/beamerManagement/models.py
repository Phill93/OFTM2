from django.db import models
from OFTM2.apps.tournament_management.models import Tournament

# Create your models here.


class Beamer(models.Model):
    name = models.TextField(
        verbose_name="Name"
    )

    VIEW_POINTS = 0
    VIEW_COMBATS = 1
    VIEW_BOTH = 2
    VIEW_CHOICES = [
        (VIEW_POINTS, 'Punkte'),
        (VIEW_COMBATS, 'Kämpfe'),
        (VIEW_BOTH, 'Punkte und Kämpfe')
    ]

    view = models.IntegerField(
        verbose_name='Anzeige',
        choices=VIEW_CHOICES,
        default=0
    )

    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.PROTECT,
        verbose_name="Tunier",
        null=True,
        blank=True
    )

    last_reload = models.DateTimeField(
        verbose_name='Letzer Reload'
    )
    def __str__(self):
        return "Beamer {}".format(self.name)

    class Meta:
        verbose_name = "Beamer"
        verbose_name_plural = "Beamer"