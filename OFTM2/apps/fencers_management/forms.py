"""Forms for fencers_management"""

from django.forms import ModelForm
from OFTM2.apps.fencers_management.models import Fencer


class FencerForm(ModelForm):
    class Meta:
        model = Fencer
        fields = ['first_name', 'last_name', 'gender', 'birthday', 'fechtpass']

    def __init__(self, *args, **kwargs):
        super(FencerForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'mdl-textfield__input'
