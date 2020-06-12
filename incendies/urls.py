
from django.urls import include, path 
from . import views
from django.conf.urls import include,url
from .views import *

urlpatterns = [
path('', views.index, name='about_incendies'),
path('database/',views.incendies_index,name= 'incendies_index'),
path('database/<int:incendie_id>/',views.incendies_detail,name= 'detail'),
path('database/<int:incendie_id>/add_intervention/', views.add_intervention, name='add_intervention'),
path('database/<int:incendie_id>/add_typeFormationincendie/', views.add_typeFormationincendie, name='add_typeFormationincendie'),
path('database/<int:incendie_id>/add_materielmobilise/', views.add_Moyen, name='add_materielmobilise'),
path('database/<int:incendie_id>/add_degat/', views.add_Degat, name='add_degat'),
path('database/create/', views.IncendieCreate.as_view(), name = 'incendie_create'),
path('database/<int:pk>/delete/', views.IncendieDeleteView.as_view(), name='incendie_delete'),
path('database/<int:pk>/update/', views.IncendieUpdateView.as_view(), name='incendie_change'),

path('database/<int:pk>/update/intervention/', views.InterventionUpdateView.as_view(), name='intervention_change'),
path('database/<int:incendie_id>/delete/intervention/<int:intervention_id>/', views.remove_intervention, name='intervention_delete'),

path('database/<int:pk>/update/moyen/', views.MoyenUpdateView.as_view(), name='moyen_change'),
path('database/<int:incendie_id>/delete/moyen/<int:moyen_id>/', views.remove_materiel, name='moyen_delete'),

path('database/<int:pk>/update/typeformation/', views.TypeFormationincendieView.as_view(), name='typeformation_change'),
path('database/<int:incendie_id>/delete/typeformation/<int:typeformationincendie_id>/', views.remove_typeformationincendie, name='typeformation_delete'),

path('database/<int:pk>/update/degat/', views.DegatView.as_view(), name='degat_change'),
path('database/<int:incendie_id>/delete/degat/<int:degat_id>/', views.remove_degat, name='degat_delete'),

url('map/', views.cartofeux, name='cartofeux'),
url('algerie/', views.algerie, name='algerie'),

url('feux/', views.feux, name='feux'),
path('graph/', views.graph, name='graph'),
path('graph/nombrefoyergraph/', views.nombrefoyergraph, name='nombrefoyergraph'),

url('pourcentage/', views.Pourcentage, name='pourcentage'),

url('synthese/', views.synthese, name='synthese'),
path('ajax/load-communes/', views.load_communes, name='ajax_load_communes'),  # <-- this one here
path('ajax/load-especes/', views.load_especes, name='ajax_load_especes'),  # <-- this one here

# path('ajax/load-wilayas/', views.load_wilayas, name='ajax_load_wilayas'),  # <-- this one here

# path('ajax/load-wilaya/', views.load_wilaya, name='ajax_load_wilaya'),  # <-- this one here
path('accounts/signup', views.signup, name='signup'),

 

]
 

# path('', views.IncendiesListView.as_view(), name='incendie_changelist'),
