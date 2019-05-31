"""definition of custom tables for django_tables2"""
import django_tables2 as tables
from OFTM2.apps.fencers_management.models import Fencer


class FencersTable(tables.Table):
    """a table for fencers"""

    class Meta:
        """meta class"""
        model = Fencer
        attrs = {
            'class': 'mdl-data-table mdl-js-data-table mdl-shadow--2dp fullwidth'
        }
        row_attrs = {
            'data-href': lambda record: record.get_absolute_url(),
            'class': 'clickable-row'
        }
        template_name = "components/tables/mdl.html"
