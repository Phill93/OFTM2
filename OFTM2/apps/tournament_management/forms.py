"""Forms for fencers_management"""

from django.forms import ModelForm

from OFTM2.apps.tournament_management.models import Tournament


class TournamentForm(ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'date', 'ageclass', 'participants']

    def __init__(self, *args, **kwargs):
        super(TournamentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'mdl-textfield__input'
