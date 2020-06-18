import os
from django.contrib.gis.utils import LayerMapping
from .models import Limite_commune
# Auto-generated `LayerMapping` dictionary for Limite_commune model
limite_commune_mapping = {
    'gid': 'gid',
    'objectid_1': 'objectid_1',
    'objectid': 'objectid',
    'objectid_2': 'objectid_2',
    'nature': 'nature',
    'name': 'name',
    'autre_nom': 'autre_nom',
    'nom_wilaya': 'nom_wilaya',
    'wilaya': 'wilaya',
    'origine': 'origine',
    'code': 'code',
    'shape_leng': 'shape_leng',
    'shape_le_1': 'shape_le_1',
    'shape_le_2': 'shape_le_2',
    'shape_area': 'shape_area',
    'geom': 'MULTIPOLYGON',
}

limite_commune_shp = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'data', 'limite_commune.shp'),
)

def run(verbose=True):
    fm = LayerMapping(Limite_commune, limite_commune_shp, limite_commune_mapping, transform=True)
    fm.save(strict=True, verbose=verbose)