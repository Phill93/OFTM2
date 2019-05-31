"""custom validators for the fencers management app"""
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy


def validate_fechtpass(value):
    """checks if the value is 6 chars long"""
    if len(value) != 9:
        raise ValidationError(
            gettext_lazy('%(value)s ist keine gültige Fechtpassnummer'),
            params={'value': value},
        )
