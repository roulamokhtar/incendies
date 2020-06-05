from django.contrib.gis import admin
from .models import *
from leaflet.admin import LeafletGeoAdmin
from import_export.admin import ImportExportModelAdmin
admin.site.register(ActionSig, LeafletGeoAdmin)
admin.site.register(Canton, LeafletGeoAdmin)
admin.site.register(Limite_commune, LeafletGeoAdmin)



 
@admin.register(nomenclature)
class ViewAdmin(ImportExportModelAdmin):
	model = nomenclature
	

 

class ActionInLine(admin.TabularInline):
	model = ActionSig
	fieldsets = [
		(LeafletGeoAdmin,{'fields':['name','volume','montant','source_financement','duree','ods', 'geom']})
	]
	extra = 0
@admin.register(Projet)
class ViewAdminProjet(ImportExportModelAdmin):
	model = Projet







 
admin.site.register(Indicateurdeclinaison)

admin.site.register(OrientationGlobale)

# admin.site.register(OrientationStrategiques)

admin.site.register(ObjectifGlobal)

# admin.site.register(ObjectifSpecifique)
 

admin.site.register(IndicateurResultat)
admin.site.register(Resultat)
admin.site.register(Action)

admin.site.register(IndicateurObjectifSpecifique)
admin.site.register(Reboisementphysique)


   

 
# admin.site.register(Forets,LeafletGeoAdmin)

admin.site.register(Piste,LeafletGeoAdmin)
admin.site.register(Point_eau,LeafletGeoAdmin)

 


 

# Register your models here. 