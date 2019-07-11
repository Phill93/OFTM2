"""Forms for fencers_management"""

from django.forms import ModelForm

from OFTM2.apps.tournament_management.models import Tournament, Combat


class TournamentForm(ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'date', 'ageclass', 'participants']

    def __init__(self, *args, **kwargs):
        super(TournamentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'mdl-textfield__input'


class CombatForm(ModelForm):
    class Meta:
        model = Combat
        fields = ['fighter1', 'fighter1_points', 'fighter2', 'fighter2_points']

    def __init__(self, *args, **kwargs):
        super(CombatForm, self).__init__(*args, **kwargs)
        self.fields['fighter1'].disabled = True
        self.fields['fighter2'].disabled = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'mdl-textfield__input'