from django.urls import include, path 
from . import views
from django.conf.urls import include,url
from .views import *
# contry_word ,piste,point_eau,maisons_forestieres,brigade,limite_commune,localites,filterCanton,zoom_commune,filterPiste,filterPoint_eau, cantons,perimetre,filterPerimetre,parcellaire,filterParcelle,filterTpf,tpf,autorisation_usage,route,foret_recreative,filterForetRecreative,cartoperimetre,cartoforetrecreative,Indicateurdeclinaison,remove_os,ee,reboisement,filterReboisement,sommephysique,sommefinance,rarfinance,montant_prevu,nbrplants,espece,odd15,oddArea,mapJijel2010,detail_cible,sous_indicateur_detail,starter,sous_indicateur_csv,starters
# ,AdViewSet from rest_framework.routers import DefaultRouter
# router = DefaultRouter()
urlpatterns = [
  



    # url('map/', HomePageView.as_view(), name='home'),

 

    path('gee/', views.odd15, name='gee'),
    path('', views.oddArea, name='odd15'),
    path('detail_cible/<str:v>/', views.detail_cible, name='detail_cible'),
    path('sous_indicateur_detail/<str:v>/', views.sous_indicateur_detail, name='sous_indicateur_detail'),

    path('mapJijel2010/', views.mapJijel2010, name='mapJijel2010'),
    path('starter/<str:v>/', views.starter, name='starter'),
    path('bokehMap/', views.bokehMap, name='bokehMap'),
    # path('starters/', views.starters, name='starters'),

    path('sous_indicateur_csv/<str:v>/', views.sous_indicateur_csv, name='sous_indicateur_csv'),



     


 

]
