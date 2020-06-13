from django.contrib.gis import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class ViewAdminWilaya(ImportExportModelAdmin):
	model = User

@admin.register(Wilaya)
class ViewAdminWilaya(ImportExportModelAdmin):
	model = Wilaya

@admin.register(Commune)
class ViewAdminCommune(ImportExportModelAdmin):
	model = Commune

admin.site.register(Moyenshumain)
admin.site.register(Limite_commune)

admin.site.register(Moyensmateriel)
admin.site.register(Degat)
admin.site.register(Typedegat)      

admin.site.register(Intervention)
admin.site.register(Organisme)


admin.site.register(TypeFormationincendie)

admin.site.register(Espece)
admin.site.register(Typeformation)

admin.site.register(Incendie)




 