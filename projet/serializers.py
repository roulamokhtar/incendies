from rest_framework_gis.serializers import (
 GeoFeatureModelSerializer
)
from .models import Canton,Limite_commune
class AdSerializer(GeoFeatureModelSerializer):
 class Meta:
	 model = Canton
	 geo_field = 'geom'
	 fields = ('id',)
class AdCommuneSerializer(GeoFeatureModelSerializer):
 class Meta:
	 model = Limite_commune
	 geo_field = 'geom'
	 fields = ('id','gid',)