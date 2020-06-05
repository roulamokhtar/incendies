from django.urls import include, path 
from . import views
from django.conf.urls import include,url
from .views import *
# contry_word ,piste,point_eau,maisons_forestieres,brigade,limite_commune,localites,feux,filterCanton,zoom_commune,filterPiste,filterPoint_eau, cantons,perimetre,filterPerimetre,parcellaire,filterParcelle,filterTpf,tpf,autorisation_usage,route,foret_recreative,filterForetRecreative,cartoperimetre,cartoforetrecreative,Indicateurdeclinaison,remove_os,ee,reboisement,filterReboisement,sommephysique,sommefinance,rarfinance,montant_prevu,nbrplants,espece,odd15,oddArea,mapJijel2010,detail_cible,sous_indicateur_detail,starter,sous_indicateur_csv,starters
# ,AdViewSet from rest_framework.routers import DefaultRouter
# router = DefaultRouter()
urlpatterns = [
    url('ee/', views.ee, name='ee'),
    #url('ee/', views.ee, name='ee'),

    # url('i/', views.ipyleaflet, name='ipyleaflet'),

    url('map/', views.carto, name='carto'),
    url('per/', views.cartoperimetre, name='cartoperimetre'),
    url('for_recreative/', views.cartoforetrecreative, name='cartoforetrecreative'),
    url('reboisement/', views.cartoreboisement, name='cartoreboisement'),
    url('world/', contry_word , name='county'),
    url('piste/', piste , name='piste'),
    url('route/', route , name='route'),
    url('point_eau/', point_eau , name='point_eau'),

    url('commune_data/',  filterCanton , name='commune_data'),
    url('filterPiste/',  filterPiste , name='filterPiste'),
    url('filterTpf/',  filterTpf , name='filterTpf'),
    url('filterPoint_eau/',  filterPoint_eau , name='filterPoint_eau'),


    url('tpf/', tpf , name='tpf'),
    url('maisons_forestieres/', maisons_forestieres , name='maisons_forestieres'),
    url('brigade/', brigade , name='brigade'),
    url('limite_commune/', limite_commune , name='limite_commune'),
    url('zoom_commune/', zoom_commune , name='zoom_commune'),
    url('localites/', localites , name='localites'),
    url('feux/', feux , name='feux'),
    url('cantons/', cantons , name='cantons'),
    url('perimetre/', perimetre , name='perimetre'),
    url('filterPerimetre/', filterPerimetre , name='filterPerimetre'),
    url('parcellaire/', parcellaire , name='parcellaire'),
    url('filterParcelle/', filterParcelle , name='filterParcelle'),

    url('foret_recreative/', foret_recreative , name='foret_recreative'),
    url('filterForetRecreative/', filterForetRecreative , name='filterForetRecreative'),
    url('reboisement/', views.reboisement , name='reboisement'),

    url('filterReboisement/', filterReboisement , name='filterReboisement'),
    url('sommephysique/', sommephysique , name='sommephysique'),
    url('sommefinance/', sommefinance , name='sommefinance'),
    url('rarfinance/', rarfinance , name='rarfinance'),
    url('montant_prevu/', montant_prevu , name='montant_prevu'),
    url('nbrplants/', nbrplants , name='nbrplants'),
    url('espece/', espece , name='espece'),



    # url('map/', HomePageView.as_view(), name='home'),

    path('', views.ProjetsListView.as_view(), name='projet_changelist'),
    path('<int:projet_id>/', views.projets_detail, name='projet_detail'),
    path('add/', views.ProjetsCreateView.as_view(), name='projet_add'),
    path('<int:pk>/update/', views.ProjetsUpdateView.as_view(), name='projet_change'),
    path('<int:pk>/delete/', views.ProjetsDeleteView.as_view(), name='projet_delete'),
    # path('<int:pk>/delete/', views.ProjetsDeleteView.as_view(), name='projet_iov'),

    path('accounts/signup', views.signup, name='signup'),


    path('histogramme', views.histogramme, name='projet_histogramme'),

    path('declinaisin', views.IndicateurdeclinaisonListView.as_view(), name='projet_changelistdeclinaison'),
    path('declinaisin/<int:projet_id>/', views.projets_detail, name='projet_declinaison_detail'),
    path('declinaisin/add/', views.IndicateurdeclinaisonCreateView.as_view(), name='projet_declinaison_add'),
    path('declinaisin/<int:pk>/update/', views.IndicateurdeclinaisonUpdateView.as_view(), name='projet_declinaison_change'),
    path('declinaisin/<int:pk>/delete/', views.IndicateurdeclinaisonDeleteView.as_view(), name='projet_declinaison_delete'),


    path('<int:projet_id>/assoc_os/<int:objectifspecifique_id>/', views.assoc_os, name='assoc_os'),
    path('<int:projet_id>/remove_os/<int:objectifspecifique_id>/', views.remove_os, name='remove_os'),

    # path('<int:projet_id>/assoc_res/<int:resultat_id>/', views.assoc_resultat, name='assoc_resultat'),
    path('<int:projet_id>/assoc_os/<int:objectifspecifique_id>/assoc_res/', views.projets_detail_res, name='projets_detail_res'),
    path('<int:projet_id>/assoc_os/<int:objectifspecifique_id>/<int:resultat_id>/', views.assoc_resultat, name='assoc_resultat'),
    path('<int:projet_id>/remove_res/<int:objectifspecifique_id>/<int:resultat_id>/', views.remove_resultat, name='remove_resultat'),

    # path('<int:projet_id>/assoc_os/<int:objectifspecifique_id>/assoc_res/action/<int:action_id>', views.projets_detail_res_action, name='projets_detail_res_action'),
    # path('<int:projet_id>/assoc_os/<int:objectifspecifique_id>/<int:resultat_id>/<int:action_id>', views.assoc_resultat_action, name='assoc_resultat_action'),
    
     # path('<int:projet_id>/add_os/', views.ObjectifSpecifiqueCreateView, name='add_os'),
    path('<int:projet_id>/assoc_os/<int:objectifspecifique_id>/assoc_res/<int:resultat_id>/actions', views.projets_detail_action, name='projets_detail_action'),
    path('<int:projet_id>/assoc_os/<int:objectifspecifique_id>/<int:resultat_id>/actions/', views.assoc_action, name='assoc_action'),

    path('sf', views.sf2035, name='sf2035'),
    path('sf/<int:orientationstrategique_id>', views.detail_objectifglobal, name='detail_objectifglobal'),
    path('sf_os/<int:orientationglobal_id>', views.detail_objectifspecifique, name='detail_objectifspecifique'),
    path('sf_res/<int:objectifspecifique_id>', views.detail_resultat, name='detail_resultat'),
    path('sf_ind_quin/<int:resultat_id>', views.detail_indicateur_quinquenat, name='detail_indicateur_quinquenat'),
    # path('markers/', views.AdViewSet, name='marker')
    path('autorisation_usage', views.autorisation_usage, name='autorisation_usage'),
    
    path('reboisements/', views.ReboisementsListView.as_view(), name='reboisement_changelist'),
    path('reboisements/<int:reboisement_id>/', views.reboisements_detail, name='reboisements_detail'),
    path('reboisements/<int:reboisement_id>/add_reboisement_physique/', views.add_reboisement_physique, name='add_reboisement_physique'),
    # path('reboisements/<int:reboisement_id>/remove_physique_reboisement/<int:reboisementphysique_id>', views.ReboisementphysiquesDeleteView, name='remove_physique_reboisement'),

    path('reboisements/<int:reboisement_id>/add_reboisement_financier/', views.add_reboisement_financier, name='add_reboisement_financier'),

    path('reboisements/add/', views.ReboisementsCreateView.as_view(), name='reboisement_add'),
    path('reboisements/<int:pk>/update/', views.ReboisementsUpdateView.as_view(), name='reboisement_change'),
    path('reboisements/<int:pk>/delete/', views.ReboisementsDeleteView.as_view(), name='reboisement_delete'),
    path('histogrammereboisement', views.histogrammeReboisement, name='reboisement_histogramme'),
    path('reboisementphysique/<int:pk>/delete/', views.ReboisementphysiquesDeleteView.as_view(), name='reboisementphysique_delete'),

      

    # path('starters/', views.starters, name='starters'),

    path('sous_indicateur_csv/<str:v>/', views.sous_indicateur_csv, name='sous_indicateur_csv'),

    path('mapJijel2010/', views.mapJijel2010, name='mapJijel2010'),


     


 

]
