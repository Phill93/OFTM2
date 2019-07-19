"""definition of custom tables for django_tables2"""
import django_tables2 as tables

from OFTM2.apps.tournament_management.models import Tournament, Combat, Points


class TournamentTable(tables.Table):
    """a table for tournaments"""

    class Meta:
        """meta class"""
        model = Tournament
        attrs = {
            'class': 'mdl-data-table mdl-js-data-table mdl-shadow--2dp fullwidth'
        }
        row_attrs = {
            'data-href': lambda record: record.get_absolute_url(),
            'class': 'clickable-row'
        }
        template_name = "components/tables/mdl.html"


class CombatTable(tables.Table):
    """a table for tournaments"""

    class Meta:
        """meta class"""
        model = Combat
        attrs = {
            'class': 'mdl-data-table mdl-js-data-table mdl-shadow--2dp fullwidth'
        }
        row_attrs = {
            'data-href': lambda record: record.get_update_url(),
            'class': 'clickable-row'
        }
        template_name = "components/tables/mdl.html"
        sequence = ('fighter1', 'fighter1_points', 'fighter2_points', 'fighter2')
        exclude = ('id', 'related_round', 'locked')


class PointsTable(tables.Table):
    """a ranking table"""

    class Meta:
        """meta class"""
        name = tables.Column(order_by=('-given', 'recieved', '-index', 'fencer_id'))
        model = Points
        attrs = {
            'class': 'mdl-data-table mdl-js-data-table mdl-shadow--2dp fullwidth'
        }
        template_name = "components/tables/mdl.html"
        exclude = {'id', 'related_round'}
        sequence = ('fencer', 'given', 'recieved', 'index')