from django.core.exceptions import FieldError
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

    def new_round(self):
        """generates a new round with combats"""
        rounds = self.round_set.order_by('round_number').all()
        round_now = rounds.last()
        if round_now:
            r = round_now.round_number + 1
        else:
            r = 1
        round_new = Round(round_number=r, tournament=self, locked=True)
        round_new.save()
        round_new.create_combats()
        return round_new

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
        try:
            original = Round.objects.get(pk=self.pk)
            if original.locked:
                raise FieldError('"{}" is locked.'.format(self.__str__()))
            super(Round, self).save(*args, **kwargs)
        except self.DoesNotExist:
            super(Round, self).save(*args, **kwargs)

    def get_round_before(self):
        if self.round_number <= 1:
            return None
        else:
            return self.tournament.round_set.get(round_number__exact=self.round_number - 1)

    def create_combats(self):
        if not self.started():
            result = []
            if self.round_number == 1:
                p = list(self.tournament.participants.order_by('?'))
            else:
                p = []
                for point in Round.objects.get(tournament=self.tournament, round_number=self.round_number-1).ranking():
                    p.append(point.fencer)

            while p:
                c = Combat(related_round_id=self.pk, fighter1=p.pop(0), fighter2=p.pop(0))
                c.save()
                result.append(c)
            return result
        else:
            raise Exception('round has already started')

    def finish(self):
        for c in self.combat_set.all():
            c.finish()

    def started(self):
        if self.combat_set.count() == 0:
            return False
        else:
            return True

    def finished(self):
        finished = True
        for c in self.combat_set.all():
            if not c.locked and c.result_set.count() == 0:
                finished = False
        return finished

    def complete(self):
        complete = True
        for c in self.combat_set.all():
            if not c.fighter2_points and not c.fighter1_points:
                complete = False
        return complete

    def ranking(self):
        return self.points_set.order_by('-given', 'recieved', '-index', 'fencer_id')

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
        verbose_name="Punkte Fechter 1",
        blank=True,
        null=True
    )

    fighter2_points = models.IntegerField(
        verbose_name="Punkte Fechter 2",
        blank=True,
        null=True
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

    def finish(self):
        if not self.locked and self.result_set.count() == 0:
            self.locked = True
            self.save()
        elif self.result_set.count() > 0:
            raise Exception('{} ist schon ausgewertet'.format(self.__str__()))
        if self.related_round.round_number > 1:
            previous_round = self.related_round.tournament.round_set.get(round_number=self.related_round.round_number-1)
            last_points = previous_round.points_set.get(fencer=self.fighter1, related_round=previous_round)
        p, created = Points.objects.get_or_create(fencer=self.fighter1, related_round=self.related_round)
        if self.related_round.round_number > 1:
            p.recieved += self.fighter2_points + last_points.recieved
            p.given += self.fighter1_points + last_points.given
        else:
            p.recieved += self.fighter2_points
            p.given += self.fighter1_points
        p.save()

        if self.related_round.round_number > 1:
            last_points = previous_round.points_set.get(fencer=self.fighter2, related_round=previous_round)
        p, created = Points.objects.get_or_create(fencer=self.fighter2, related_round=self.related_round)
        if self.related_round.round_number > 1:
            p.recieved += self.fighter1_points + last_points.recieved
            p.given += self.fighter2_points + last_points.given
        else:
            p.recieved += self.fighter1_points
            p.given += self.fighter2_points
        p.save()

    def save(self, *args, **kwargs):
        try:
            original = Combat.objects.get(pk=self.pk)
            if original.locked:
                raise FieldError('"{}" is locked.'.format(self.__str__()))
            super(Combat, self).save(*args, **kwargs)
        except self.DoesNotExist:
            super(Combat, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Kampf"
        verbose_name_plural = "Kämpfe"


class Result(models.Model):
    related_round = models.ForeignKey(
        Round,
        on_delete=models.CASCADE,
        verbose_name="Runde"
    )
    combat = models.ForeignKey(
        Combat,
        on_delete=models.PROTECT,
        verbose_name="Kampf"
    )
    winner = models.ForeignKey(
        Fencer,
        on_delete=models.PROTECT,
        verbose_name="Sieger",
        related_name="+"
    )
    looser = models.ForeignKey(
        Fencer,
        on_delete=models.PROTECT,
        verbose_name="Verlierer",
        related_name="+"
    )
    winner_given = models.IntegerField(
        verbose_name="Sieger gegeben"
    )
    winner_received = models.IntegerField(
        verbose_name="Sieger erhalten"
    )
    looser_given = models.IntegerField(
        verbose_name="Verlierer gegben"
    )
    looser_received = models.IntegerField(
        verbose_name="Verlierer erhalten"
    )

    class Meta:
        verbose_name = "Ergebniss"
        verbose_name_plural = "Ergebnisse"


class Points(models.Model):
    related_round = models.ForeignKey(
        Round,
        on_delete=models.CASCADE,
        verbose_name="Runde"
    )
    fencer = models.ForeignKey(
        Fencer,
        on_delete=models.CASCADE,
        verbose_name="Fechter"
    )
    recieved = models.IntegerField(
        verbose_name="Erhaltene Treffer",
        default=0
    )
    given = models.IntegerField(
        verbose_name="Gegebene Treffer",
        default=0
    )

    index = models.IntegerField(
        verbose_name="Index",
        default=0
    )

    def save(self, *args, **kwargs):
        self.index = self.given - self.recieved
        super(Points, self).save(*args, **kwargs)

    def __str__(self):
        return "Punkte für {}".format(self.fencer)

    class Meta:
        verbose_name = "Punkte"
        verbose_name_plural = "Punkte"