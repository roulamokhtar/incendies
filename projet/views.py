# Create your views here.
from django.shortcuts import render, redirect ,get_list_or_404, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, TemplateView, DetailView, DeleteView
from django.urls import reverse_lazy
from .models import *
from .forms import ActionForm , ProjetForm , ObjectifSpecifiqueForm,IndicateurdeclinaisonForm ,ReboisementForm,ReboisementphysiqueForm,ReboisementfinanceForm
from django.forms import modelformset_factory , inlineformset_factory
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.http import HttpResponse,JsonResponse
from django.template import loader
from django.core.paginator import Paginator
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_gis.filters import InBBoxFilter
from .serializers import AdSerializer,AdCommuneSerializer
from django.contrib.gis.geos import GEOSGeometry,Polygon
from django.db import connection
from django.contrib.gis.db.models.functions import Intersection  
from django.db.models.functions import Coalesce
from django.db.models import Subquery,OuterRef,Sum,Count,Max,Value as V ,FloatField
from django.db import connection
import json
import time
import requests
import csv
# from projet import integration
import ee
import pandas as pd
import geopandas as gpd
from bokeh.plotting import ColumnDataSource, figure, output_file, show
from bokeh.embed import components
from bokeh.models import Slider, HoverTool, GeoJSONDataSource,ColumnDataSource,LassoSelectTool,WheelZoomTool,Circle,Line,Rect,Text,Plot,LinearColorMapper,ColorBar
from bokeh.models.tools import HoverTool
from bokeh.palettes import Spectral6
from bokeh.tile_providers import CARTODBPOSITRON, get_provider,Vendors
from bokeh.io import output_notebook, show, output_file,curdoc
from bokeh.palettes import brewer

from bokeh.layouts import widgetbox, row, column
     
# import branca.colormap as cm
import os
import json

# from eeconvert import eeImageToFoliumLayer as ee_plot
# import webbrowser
# import ee.mapclient
import math
import datetime

from folium.folium import Map

# from IPython.display import HTML



class AdViewSet(ReadOnlyModelViewSet):
 bbox_filter_field = 'geom'
 filter_backends = (InBBoxFilter,)
 queryset = Canton.objects.filter(geom__isnull=False)
 serializer_class = AdSerializer

@login_required
def index(request):
     return render(request,'projet/index.html')
@login_required
def autorisation_usage(request):

     return render(request,'projet/autorisation_usage.html')
@login_required    
def sf2035(request):
    orientationstrategiques = OrientationStrategiques.objects.all()
    return render(request,'projet/sf.html',{
    'orientationstrategiques':orientationstrategiques,
    })
@login_required
def detail_objectifglobal(request,orientationstrategique_id):
    orientationstrategique = OrientationStrategiques.objects.get(id=orientationstrategique_id)

    orientationglobales = ObjectifGlobal.objects.filter(orientationstrategique=orientationstrategique)
 
    return render(request,'projet/sf_orientationglobales.html',{
    'orientationglobales':orientationglobales,
    'orientationstrategique':orientationstrategique
    })
@login_required
def detail_objectifspecifique(request,orientationglobal_id):
    objectifglobal = ObjectifGlobal.objects.get(id=orientationglobal_id)

    objectifspecifiques = ObjectifSpecifique.objects.filter(objectifglobal=objectifglobal)
 
    return render(request,'projet/sf_objectifspecifiques.html',{
    'objectifspecifiques':objectifspecifiques,
    'objectifglobal':objectifglobal
    })
@login_required
def detail_resultat(request,objectifspecifique_id):
    objectifspecifique = ObjectifSpecifique.objects.get(id=objectifspecifique_id)

    resultats = Resultat.objects.filter(objectifspecifique=objectifspecifique)
 
    return render(request,'projet/sf_resultats.html',{
    'resultats':resultats,
    "objectifspecifique":objectifspecifique
    })
@login_required
def detail_indicateur_quinquenat(request,resultat_id):
    resultats = Resultat.objects.get(id=resultat_id)

    ind_quequenat = Indicateurdeclinaison.objects.filter(resultat_id=resultats)
 
    return render(request,'projet/sf_indicateur_quinquenat.html',{
    'resultats':resultats,
    "indicateur_quequenat":ind_quequenat
    })

 
      
def carto(request):
    canton =  Canton.objects.filter(layer__contains='FD')
    communes =  Limite_commune.objects.all()
    perimetres =  Perimetre.objects.all()
    beneficiares = Parcellaire_perimetre.objects.all()
    foret_recreatives = Foret_recreative.objects.all()
    reboisements = Reboisement.objects.filter(kml_folder__contains='Programme 2017')
 
    return render(request,'projet/layoutmap.html',
    {
    'Canton':canton,
    'communes':communes,
    'perimetres':perimetres,
    'beneficiares':beneficiares,
    'foret_recreatives':foret_recreatives,
    'reboisements':reboisements,
   
    } ) 
def cartoperimetre(request):
    canton =  Canton.objects.filter(layer__contains='FD')
    communes =  Limite_commune.objects.all()
    perimetres =  Perimetre.objects.all()
    beneficiares = Parcellaire_perimetre.objects.all()
    foret_recreatives = Foret_recreative.objects.all()
    return render(request,'projet/layoutmapPerimetre.html',
    {
    'Canton':canton,
    'communes':communes,
    'perimetres':perimetres,
    'beneficiares':beneficiares,
    'foret_recreatives':foret_recreatives,

    } ) 

def cartoforetrecreative(request):
    canton =  Canton.objects.filter(layer__contains='FD')
    communes =  Limite_commune.objects.all()
    perimetres =  Perimetre.objects.all()
    beneficiares = Parcellaire_perimetre.objects.all()
    foret_recreatives = Foret_recreative.objects.all()

    return render(request,'projet/layoutmapForetRecreative.html',
    {
    'Canton':canton,
    'communes':communes,
    'perimetres':perimetres,
    'beneficiares':beneficiares,
    'foret_recreatives':foret_recreatives,


    } ) 

def cartoreboisement(request):
    canton =  Canton.objects.filter(layer__contains='FD')
    communes =  Limite_commune.objects.all()
    perimetres =  Perimetre.objects.all()
    beneficiares = Parcellaire_perimetre.objects.all()
    foret_recreatives = Foret_recreative.objects.all()
    reboisements = Reboisement.objects.filter(kml_folder__contains='Programme 2017')

    return render(request,'projet/layoutmapReboisement.html',
    {
    'Canton':canton,
    'communes':communes,
    'perimetres':perimetres,
    'beneficiares':beneficiares,
    'foret_recreatives':foret_recreatives,
    'reboisements':reboisements,

    } ) 


def contry_word(request):
    cantons = serialize('geojson', Canton.objects.all())
    return HttpResponse(cantons,content_type='json')
def piste(request):
    pistes = serialize('geojson', Piste.objects.all())
    return HttpResponse(pistes,content_type='json')
def point_eau(request):
    point_eau =  Point_eau.objects.all()
    point_eau = serialize('geojson',point_eau)
    return HttpResponse(point_eau,content_type='json')
def tpf(request):
    tpf = serialize('geojson', Tpf.objects.all())
    return HttpResponse(tpf,content_type='json')
def maisons_forestieres(request):
    maisons_forestieres = serialize('geojson', Maison_forestiere.objects.all())
    return HttpResponse(maisons_forestieres,content_type='json')
def brigade(request):
    brigade = serialize('geojson', Brigade.objects.all())
    return HttpResponse(brigade,content_type='json')
def limite_commune(request):
    limite_communes = serialize('geojson', Limite_commune.objects.all())
    return HttpResponse(limite_communes,content_type='json')



    
def localites(request):
    localites = serialize('geojson', Localites.objects.all())
    return HttpResponse(localites,content_type='json')

def feux(request):
    feux = serialize('geojson', Incendie.objects.all())
    return HttpResponse(feux,content_type='json')

def route(request):
    routes = serialize('geojson', Route1.objects.all())
    return HttpResponse(routes,content_type='json')

def cantons(request):
    localites = serialize('geojson', Canton.objects.exclude(name__isnull=True))
    # .exclude(name__isnull=True)
    return HttpResponse(localites,content_type='json')
def perimetre(request):
    perimetres = serialize('geojson', Perimetre.objects.all())
    return HttpResponse(perimetres,content_type='json')
def parcellaire(request):
    parcelles  = serialize('geojson', Parcellaire_perimetre.objects.all())
    return HttpResponse(parcelles,content_type='json')
def foret_recreative(request):
    foret_recreative  = serialize('geojson', Foret_recreative.objects.all())
    return HttpResponse(foret_recreative,content_type='json')
def reboisement(request):
    reboisement  = serialize('geojson', Reboisement.objects.filter(kml_folder__contains='Programme 2017'))
    return HttpResponse(reboisement,content_type='json')

# def ProjetsListView(request):
#     template = loader.get_template('projet/projets_list.html')
#     model = Projets
#     context_object_name = 'people'
#     return HttpResponse(template.render(request=request))

def filterCanton(request):
    cantons= Canton.objects.all()
    if request.method == 'POST':
        x = request.POST.get('gid')
        cursor = connection.cursor()
        cursor.execute("SELECT  ST_AsGeoJSON(ST_Intersection(i.geom, l.geom)) ::JSON AS geometry,i.name as name,l.name as commune , ST_Area(ST_Transform(ST_INTERSECTION(i.geom, l.geom),30731)::geometry)   as superficie FROM   projet_canton i,projet_limite_commune l WHERE ST_Intersects(i.geom, l.geom)  AND i.name is not null  AND l.gid =  %s", [x])
        result = cursor.fetchall()   
        return   JsonResponse(result , safe=False)
    else:
        commune_selected = serialize('geojson', cantons)
        return HttpResponse(commune_selected, content_type='json') 
             
def filterPiste(request):
    if request.method == 'POST':
        x = request.POST.get('gid')
        cursor = connection.cursor()
        cursor.execute("SELECT  ST_AsGeoJSON(ST_Intersection(i.geom, l.geom)) ::JSON AS geometry,i.name as name,l.name as commune ,ST_LENGTH(ST_Transform(ST_Intersection(i.geom, l.geom),30731)::geometry) as longeur FROM   projet_piste i,projet_limite_commune l WHERE ST_Intersects(i.geom, l.geom) AND   l.gid =  %s", [x])
        result = cursor.fetchall()
         
        return   JsonResponse(result , safe=False)
    else:
        commune_selected = serialize('geojson', Limite_commune.objects.all())

            # pointc =  Point_eau.objects.filter(geom__within=commune_selected)
    
    return HttpResponse(commune_selected, content_type='json') 
def filterTpf(request):
    if request.method == 'POST':
        x = request.POST.get('gid')
        cursor = connection.cursor()
        cursor.execute("SELECT  ST_AsGeoJSON(ST_Intersection(i.geom, l.geom)) ::JSON AS geometry,i.tenant as name,l.name as commune, ST_Area(ST_Transform(ST_INTERSECTION(i.geom, l.geom),30731)::geometry)  as superficie FROM   projet_Tpf i,projet_limite_commune l WHERE ST_Intersects(i.geom, l.geom) AND   l.gid =  %s", [x])
        result = cursor.fetchall()
         
        return   JsonResponse(result , safe=False)
    else:
        commune_selected = serialize('geojson', Limite_commune.objects.all())

            # pointc =  Point_eau.objects.filter(geom__within=commune_selected)
    
    return HttpResponse(commune_selected, content_type='json') 
def filterPerimetre(request):
    perimetres= Perimetre.objects.all()
    if request.method == 'POST':
        x = request.POST.get('id')
        perimetre = Perimetre.objects.filter(id=x)
        commune_selected = serialize('geojson', perimetre)

    else:

        commune_selected = serialize('geojson', perimetres)
    
    return HttpResponse(commune_selected, content_type='json')  
def filterParcelle(request):
    parcelles= Parcellaire_perimetre.objects.all()
    if request.method == 'POST':
        x = request.POST.get('id')
        parcelles = Parcellaire_perimetre.objects.filter(id=x)
        commune_selected = serialize('geojson', parcelles)

    else:

        commune_selected = serialize('geojson', parcelles)
    
    return HttpResponse(commune_selected, content_type='json')

def filterForetRecreative(request):
    foret_recreative= Foret_recreative.objects.all()
    if request.method == 'POST':
        x = request.POST.get('id')
        foret_recreative = Foret_recreative.objects.filter(id=x)
        foret_recreative_selected = serialize('geojson', foret_recreative)

    else:

        foret_recreative_selected = serialize('geojson', foret_recreative)
    
    return HttpResponse(foret_recreative_selected, content_type='json')  
def filterReboisement(request):
 
    reboisement= Reboisement.objects.filter(kml_folder__contains='Programme 2017')
    if request.method == 'POST':
        x = request.POST.get('id')
        reboisement = Reboisement.objects.filter(id=x)
 
        reboisement_selected = serialize('geojson', reboisement)

    else:

        reboisement_selected = serialize('geojson', reboisement)
    
    return HttpResponse(reboisement_selected, content_type='json')  

def filterPoint_eau(request):
    if request.method == 'POST':
        x = request.POST.get('gid')
        communes = Limite_commune.objects.get(gid= x)
        point_eau =  Point_eau.objects.filter(geom__within=communes.geom)
        commune_selected = serialize('geojson', point_eau)
    else:
        commune_selected = serialize('geojson', Limite_commune.objects.all())

    return HttpResponse(commune_selected,content_type='json') 
        

#         departements = Departement.objects.filter(geom__intersects=bbox)
# departements = departements.annotate(clipped=Intersection('geom', bbox))
       
def zoom_commune(request):
    if request.method == 'POST':
        x = request.POST.get('gid')
       
        commune_selected = serialize('geojson', Limite_commune.objects.filter(gid=x)) 
    
    return HttpResponse(commune_selected, content_type='json')  
      

class ProjetsListView(LoginRequiredMixin,ListView):  
    template_name = 'projet/projets_list.html'
    model = Projet
    paginate_by = 9
    ordering = ['annee','commune']
    context_object_name = 'people'
    def get_queryset(self):
        queryset = super(ProjetsListView, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class ProjetsCreateView(LoginRequiredMixin,CreateView):
    model = Projet
    form_class = ProjetForm
    success_url = reverse_lazy('projet_changelist')
    def form_valid(self,form):
        # assigné the logged in user (self.request.user)
        form.instance.user = self.request.user
        # let the CreateView do its job as usual
        return super().form_valid(form)

class ProjetsUpdateView(LoginRequiredMixin,UpdateView):
    model = Projet
    form_class = ProjetForm
 
class ProjetsDeleteView(LoginRequiredMixin,DeleteView):
    model = Projet
    form_class = ProjetForm
    success_url = reverse_lazy('projet_changelist')

def signup(request):
    error_message =''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # this is how we login 
            login(request, user)
            return redirect('/')
        else:
            error_message = ' Invalid sign up retry again'
    # a  bad POST or a GET request so render signup.html  with an empty template
    form = UserCreationForm()
    context = {
    'form': form,
    'error_message': error_message
    }
    return render(request,'registration/signup.html', context)
    #//////////////////////////////////////////////////////
@login_required
def histogramme(request):
    # queryset = Projet.objects.all().annotate(dcount=Count('commune'))
    queryset1 = Limite_commune.objects.annotate(nombre_objectifglobal= Count('projet__objectifglobal'))

    queryset2 =ObjectifGlobal.objects.annotate(nombre =Count('projet__objectifglobal')).filter(nombre__gt = 1) 
 
    return render(request,'projet/histogramme.html',{
                    'queryset':queryset1, 
                    'queryset2':queryset2
                      

        })
#////////////////////////////////////////////////////////
@login_required
def mapJijel2010(request):
    return render(request,'projet/mapJijel2010.html')

#/////////////////////////////////
#//////////////////////REBOISEMENT/////////////////////////////
class ReboisementsListView(ListView):
    queryset= Reboisement.objects.filter(kml_folder='Programme 2017')
    template_name = 'projet/reboisement_list.html'
    model = Reboisement
    paginate_by = 100
    ordering = ['commune']
    context_object_name = 'people'


class ReboisementsCreateView(CreateView):
    model = Reboisement
    form_class = ReboisementForm
    success_url = reverse_lazy('reboisement_changelist')

class ReboisementsUpdateView(UpdateView):
    model = Reboisement
    form_class = ReboisementForm
 
class ReboisementsDeleteView(DeleteView):
    model = Reboisement
    form_class = ReboisementForm
    success_url = reverse_lazy('reboisement_changelist')

def reboisements_detail(request, reboisement_id):
    reboisement = Reboisement.objects.get(id=reboisement_id)
    sommePhysique = Reboisementphysique.objects.filter(reboisement__id=reboisement_id).aggregate(somme = Sum('realisation_physique'))
    sommeFinance = Reboisementfinancier.objects.filter(reboisement__id=reboisement_id).aggregate(somme = Sum('paiement'))

    # instantiate a ReboisementphysiqueForm
    reboisement_physiqueForm = ReboisementphysiqueForm()
    reboisement_financeForm = ReboisementfinanceForm()
    #filtrer les objectifs specifique lié a l'objectif global
    # objectifG=projet.objectifglobal
    # os_projet_relie_objectif_global = ObjectifSpecifique.objects.filter(objectifglobal=objectifG)
    # os_projet_doesnt_have = os_projet_relie_objectif_global.exclude(id__in=projet.objectifspecifique.all().values_list('id'))
 
    return render(request,'projet/reboisement_detail.html',{
        'reboisement':reboisement,
        'reboisement_physiqueForm':reboisement_physiqueForm,
        'reboisement_financeForm':reboisement_financeForm,
        'sommePhysique':sommePhysique,
        'sommeFinance':sommeFinance
        # 'obspecifiques':os_projet_doesnt_have,
        # 'objectifG':objectifG,
        # 'os_projet_relie_objectif_global':os_projet_relie_objectif_global
          })
def sommephysique(request):

    if request.method == 'POST':
       
        x = request.POST.get('id')
        sommePhysique = Reboisement.objects.filter(id=x).aggregate(Sum('reboisementphysique__realisation_physique')).values()
    return HttpResponse(sommePhysique, content_type='json')
def nbrplants(request):

    if request.method == 'POST':
       
        x = request.POST.get('id')
        rar = Reboisement.objects.filter(id=x).aggregate( nbrplants = Sum('reboisementphysique__realisation_physique', output_field=FloatField())*Max('densite',output_field=FloatField()))
    return HttpResponse(rar['nbrplants'], content_type='json')
 
def sommefinance(request):
    if request.method == 'POST':
        x = request.POST.get('id')
        sommeFinance = Reboisement.objects.filter(id=x).aggregate(sommefinance=Coalesce(Sum('reboisementfinancier__paiement'),V(0))).values()
        
    return HttpResponse(sommeFinance, content_type='json') 
def rarfinance(request):
    if request.method == 'POST':
        x = request.POST.get('id')
        rar = Reboisement.objects.filter(id=x).aggregate( montant_diff = Max('montant_ma', output_field=FloatField())- Sum('reboisementfinancier__paiement',output_field=FloatField()))
    return HttpResponse(rar['montant_diff'], content_type='json')  

def montant_prevu(request): 
    if request.method == 'POST':
        x = request.POST.get('id')
        montant_prevu = Reboisement.objects.filter(id=x).aggregate(montant_prevu = Max('montant_ma'))

    return HttpResponse(montant_prevu['montant_prevu'], content_type='json')
def espece(request): 
    if request.method == 'POST':
        x = request.POST.get('id')
        field_name = 'espece'
        obj = Reboisement.objects.filter(id=x).first()
        field_value = getattr(obj, field_name)
        # d = serialize('json',field_value)
      
    return HttpResponse(field_value, content_type='text')
 

  

    
  

def add_reboisement_physique(request, reboisement_id):
    # create an instance of ReboisementphysiqueForm
    formphysique = ReboisementphysiqueForm(request.POST)
    # VALIDATE THE FORM
    if formphysique.is_valid():
        new_physique = formphysique.save(commit=False)
        new_physique.reboisement_id = reboisement_id
        new_physique.save()
      
    return redirect('reboisements_detail', reboisement_id=reboisement_id)

def add_reboisement_financier(request, reboisement_id):
    # create an instance of ReboisementphysiqueForm
    formfinanciere = ReboisementfinanceForm(request.POST)
    # VALIDATE THE FORM
    if formfinanciere.is_valid():
        new_finance = formfinanciere.save(commit=False)
        new_finance.reboisement_id = reboisement_id
        new_finance.save()
      
    return redirect('reboisements_detail', reboisement_id=reboisement_id)

def histogrammeReboisement(request):
    queryset = Reboisement.objects.filter(kml_folder='Programme 2017').annotate(sum_physique=Coalesce(Sum('reboisementphysique__realisation_physique'), V(0))) 
    queryset2 = Reboisement.objects.filter(kml_folder='Programme 2017').annotate(sum_paiement=Coalesce(Sum('reboisementfinancier__paiement'), V(0))) 

    # queryset2 =ObjectifGlobal.objects.annotate(nombre =Count('projet__objectifglobal')).filter(nombre__gt = 1) 
    return render(request,'projet/histogrammeReboisement.html',{
                    # 'queryset':queryset1, 
                    'queryset':queryset,
                    'queryset2':queryset2
                       
        })

# def reboisements_mise_en_Oeuvre_Physique(request):
#     # reboisement = Reboisement.objects.get(id=reboisement_id)
#     # sommePhysique = Reboisementphysique.objects.filter(reboisement__id=reboisement_id).aggregate(somme = Sum('realisation_physique'))
#     # sommeFinance = Reboisementfinancier.objects.filter(reboisement__id=reboisement_id).aggregate(somme = Sum('paiement'))
#     # return 

#     if request.method == 'POST':
#         x = request.POST.get('id')
#         # reboisement = Reboisement.objects.filter(id=x)
#         # reboisement = Reboisement.objects.filter(id=x).aggregate(somme = Sum('reboisementphysique__realisation_physique'))
#         # reboisement = Reboisement.objects.get(id=x).aggregate(somme=Sum('reboisementphysique__realisation_physique')).values('espece','nbr_plants', 'somme')
#         reboisement = Reboisementphysique.objects.values('reboisement__name','reboisement__espece').annotate(somme = Sum('realisation_physique')).filter(id = 1).only('realisation_physique','reboisement__espece')

#         reboisement_selected = serialize('geojson', reboisement)
#     # else:

#     #     reboisement_selected = serialize('geojson', reboisement)
    
#     return HttpResponse(reboisement_selected, content_type='json')
#///////////////fin REBOISEMENT////////////////////////////////////////////////
#/////////////// REBOISEMENT PHYSIQUE////////////////////////////////////////////////

class ReboisementphysiquesListView(ListView):
    queryset= Reboisementphysique.objects.all()
    template_name = 'projet/reboisementphysique_list.html'
    model = Reboisementphysique
    paginate_by = 9
    ordering = ['date']
    context_object_name = 'people'


class ReboisementphysiquesCreateView(CreateView):
    model = Reboisementphysique
    form_class = ReboisementphysiqueForm
    success_url = reverse_lazy('reboisementphysique_changelist')

class ReboisementphysiquesUpdateView(UpdateView):
    model = Reboisementphysique
    form_class = ReboisementphysiqueForm
 
class ReboisementphysiquesDeleteView(DeleteView):
    model = Reboisementphysique
    form_class = ReboisementphysiqueForm
    success_url = reverse_lazy('reboisement_changelist')
   # /////////////////////////////////////fin REBOISEMENT PHYSIQUE////////////////////////////////////////


class IndicateurdeclinaisonListView(ListView):
    queryset= Indicateurdeclinaison.objects.all() 
    template_name = 'projet/projets_indicateur_list.html'
    model = Indicateurdeclinaison
    
    context_object_name = 'peopledeclinaison'


class IndicateurdeclinaisonCreateView(CreateView):
    model = Indicateurdeclinaison
    form_class = IndicateurdeclinaisonForm
    success_url = reverse_lazy('projet_changelistdeclinaison')

class IndicateurdeclinaisonUpdateView(UpdateView):
    model = Indicateurdeclinaison
    form_class = IndicateurdeclinaisonForm
 
class IndicateurdeclinaisonDeleteView(DeleteView):
    model = Indicateurdeclinaison
    form_class = IndicateurdeclinaisonForm
    success_url = reverse_lazy('projet_changelistdeclinaison')



   # /////////////////////////////////////////////////////////////////////////////


# class ProjetsDetailView(DetailView,projet_id):
#     model = Projets.objects.get(id=projet_id)  
#     template_name = 'projet/projet_detail.html'

    # form_class = ProjetForm
@login_required
def projets_detail(request, projet_id):
    projet = Projet.objects.get(id=projet_id)
    #filtrer les objectifs specifique lié a l'objectif global
    objectifG=projet.objectifglobal
    os_projet_relie_objectif_global = ObjectifSpecifique.objects.filter(objectifglobal=objectifG)
    os_projet_doesnt_have = os_projet_relie_objectif_global.exclude(id__in=projet.objectifspecifique.all().values_list('id'))
 
    return render(request,'projet/projet_detail.html',{
        'projet':projet,
        'obspecifiques':os_projet_doesnt_have,
        'objectifG':objectifG,
        'os_projet_relie_objectif_global':os_projet_relie_objectif_global
          })
def projets_detail_res(request, projet_id,objectifspecifique_id):
    projet = Projet.objects.get(id=projet_id)
    projet_os = ObjectifSpecifique.objects.get(id=objectifspecifique_id)

    #filtrer les resultat lié a lobjectifs specifique
    # 1 avoir l'objectif specifique voulu
 
    resultat_general= Resultat.objects.filter(objectifspecifique = projet_os)
    resultat_projet_doesnt_have = resultat_general.exclude(id__in=projet.resultat.all().values_list('id'))
 
    return render(request,'projet/projet_resultats.html',{
        'projet':projet,
        'os':projet_os,
        'resultats':resultat_projet_doesnt_have,
        'resultat_general':resultat_general

          })
def projets_detail_action(request, projet_id,objectifspecifique_id, resultat_id):
    projet = Projet.objects.get(id=projet_id)
    projet_os = ObjectifSpecifique.objects.get(id=objectifspecifique_id)
    projet_resultat = Resultat.objects.get(id=resultat_id)

    #filtrer les resultat lié a lobjectifs specifique
    # 1 avoir l'objectif specifique voulu
        # 2 avoir le resultat voulu

    #instantiate ActionForm
    action_form = ActionForm()
     

    action_general= Action.objects.all()
    actions_projet_doesnt_have = action_general.exclude(id__in=projet.action_set.all().values_list('id'))
 
    return render(request,'projet/projet_actions.html',{
        'projet':projet,
        'os':projet_os,
        'resultats':projet_resultat,
        'actions':actions_projet_doesnt_have,
        'action_form' : action_form

          })
    
###############################################################
 

def ObjectifSpecifiqueDetail(request, objectifspecifique_id):
    objectifspecifiques = ObjectifSpecifique.objects.get(id=objectifspecifique_id)
    #instatiate objectifspecifiqurForm
    
    return render(request,'projet/ObjectifSpecifique_form.html',{
        'objectifspecifiques':objectifspecifiques
         })
def assoc_os(request, projet_id, objectifspecifique_id):
    Projet.objects.get(id=projet_id).objectifspecifique.add(objectifspecifique_id)
    return redirect('projet_detail', projet_id=projet_id)


def remove_os(request, projet_id, objectifspecifique_id):
    Projet.objects.get(id=projet_id).objectifspecifique.remove(objectifspecifique_id)
    return redirect('projet_detail', projet_id=projet_id)
    

def assoc_resultat(request, projet_id,objectifspecifique_id, resultat_id):
    Projet.objects.get(id=projet_id,objectifspecifique=objectifspecifique_id).resultat.add(resultat_id)
    return redirect('projets_detail_res', projet_id=projet_id, objectifspecifique_id= objectifspecifique_id)

def remove_resultat(request, projet_id,objectifspecifique_id, resultat_id):
    Projet.objects.get(id=projet_id,objectifspecifique=objectifspecifique_id).resultat.remove(resultat_id)
    return redirect('projets_detail_res', projet_id=projet_id, objectifspecifique_id= objectifspecifique_id)

def assoc_action(request, projet_id,objectifspecifique_id, resultat_id):
    form =  ActionForm(request.POST)
    # validate the form
    if form.is_valid():
        new_action= form.save(commit=False)
        new_action.projet_id= projet_id
        new_action.resultat_id= resultat_id
        new_action.save()
        new_action=form
 
    return redirect('projets_detail_action', projet_id=projet_id, objectifspecifique_id= objectifspecifique_id,resultat_id=resultat_id)



def ee(request):

    return render(request,'projet/layoutearthengine.html' )

def remove_physique_reboisement(request, reboisement_id, reboisementphysique_id):
    Reboisement.objects.get(id=reboisement_id).reboisementphysique.remove(reboisementphysique_id)
    return redirect('reboisements_detail', reboisement_id=reboisement_id )

 

def oddArea(request):
    response = requests.get('https://unstats.un.org/SDGAPI/v1/sdg/Goal/15/Target/List?includechildren=true')
    geodata = response.json()
    odd15 = {
    "code": geodata[0]['code'],
    "title": geodata[0]['title'],
    "description": geodata[0]['description'],
    'uri': geodata[0]['uri'],
    "odd15":geodata[0],
    "goal": geodata[0]['targets'],
 
    }
    print (odd15['goal'])
    context = {'odd15': odd15}
    return render(request, 'projet/odd15.html',  context)
def detail_cible(request,v):
    url = 'https://unstats.un.org/SDGAPI/v1/sdg/Indicator/{}/Series/List'
    r = requests.get(url.format(v)).json()
    print(r)
    indicateurs = {
    "code": r,
    "series": r[0]['code']
    }
    context = {'indicateurs': indicateurs }
    return render(request, 'projet/cible_detail.html',  context)

def sous_indicateur_detail(request,v):
    # url = 'https://unstats.un.org/SDGAPI/v1/sdg/Indicator/{}/Series/List'
    # url = 'https://unstats.un.org/SDGAPI/v1/sdg/Series/{}/GeoArea/12/DataSlice'
    url = 'https://unstats.un.org/SDGAPI/v1/sdg/Series/Data?seriesCode={}&areaCode=12'
    r = requests.get(url.format(v)).json()
    print(json.dumps(r,indent= 2))
    sous_indicateurs = {
    "code": r,
    "seriesDescription": r['data'][0]['seriesDescription'],
    "geoAreaCode": r['data'][0]['geoAreaCode'],

    "series": v,
    "footnotes": r['data'][0]['footnotes'][0],
    "source": r['data'][0]['source'],
    "data": r['data'],
    "indicateur":r['data'][0]['indicator'][0]
    }
    print(sous_indicateurs['indicateur'])
    context = {'sous_indicateurs': sous_indicateurs }
    return render(request, 'projet/sous_indicateur_detail.html',  context)
def sous_indicateur_csv(request,v):
    
    url = 'https://unstats.un.org/SDGAPI/v1/sdg/Series/Data?seriesCode={}&areaCode=12'
    r = requests.get(url.format(v)).json()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename='+r['data'][0]['seriesDescription']+'.csv' 
    writer = csv.writer(response)
    writer.writerow( ["année" , "valeur","unite"])
    for item in r['data']:
        writer.writerow( [item['timePeriodStart'] , item['value'],item['attributes']['Units']])
    return response
def starter(request,v):

    url = 'https://unstats.un.org/SDGAPI/v1/sdg/Series/Data?seriesCode={}&areaCode=12'
    r = requests.get(url.format(v)).json()
    zz = [] # sur l'axe vertical les valeurs
    xx = [] # sur l'axe horizental

    for sd in r["data"]:
         zz.append(sd['value'])
         xx.append(sd["timePeriodStart"])
    xx = list(map(str, xx))
    print(zz)
    print(xx)
    titre = r['data'][0]['seriesDescription']
    label = r['data'][0]['indicator'][0]
   
    p = figure(x_range= xx,plot_height= 550,plot_width= 1200, title=titre,toolbar_location = "below", tools = "pan,wheel_zoom,box_zoom,reset,tap,crosshair" )
    source = ColumnDataSource(data = dict(xx=xx, zz=zz, color=Spectral6))
    # p.add_tools(LassoSelectTool())
    # p.add_tools(WheelZoomTool())
    p.vbar(x='xx',top='zz', width=.5, color ='color',source = source)
    # p.legend.orientation = "horizontal"
    # p.legend.location= "top_center"

    # p.xgrid.grid_line_color = "black"
    # p.y_range.start =0
    # p.line(x=xx,y=zz, color="black", line_width=2)

    # add  Tooltips

    hover = HoverTool()
    hover.tooltips="""
        <div>
            <h3>@xx<h/3>
            <div><strong><Valeur:</strong>@zz</div>
        </div>
    """
    p.add_tools(hover)
    # p = figure(

    #     y_range = xx,
    #     plot_width = 900,
    #     plot_height= 500,

    #     title="indicateur :"+label + ": "+"Code serie :"+titre,
    #     x_axis_label= label,
    #     tools ="pan,box_select,zoom_in, zoom_out,save,reset"
    #  )
    # # render a glyph
    # p.hbar(
    #     y =xx,
    #     right= zz,
    #     left=0,
    #     height=0.4,
    #     color='green',
    #     fill_alpha=0.5

    # )
    script , div = components(p)
    return render(request,'projet/starter.html', {'script':script, 'div':div})         

def bokehMap(request):
    algerie = os.path.join('projet/data', 'gadm_jijel.geojson')
    # fname = 'NILZone.shp'
    algerie_geo = gpd.read_file(algerie)
    algerie_geo=algerie_geo[['NAME_1','NAME_2','geometry']]
    # print(nil.head())
    loss_algerie = os.path.join('projet/data','loss_jijel_10.csv')
    algerie_data = pd.read_csv(loss_algerie,encoding="ISO-8859-1")
    # jijel_data['COMMUNE']=jijel_data['SUBNATIONAL2']

    # jijel_data=jijel_data[['SUBNATIONAL1','COMMUNE','SUBNATIONAL2','TC_LOSS_HA_']]
    # print(jijel_data.head())
    # commloss2017 = nil.merge(jijel_data, left_on = 'COMMUNE', right_on = 'SUBNATIONAL2', how = 'left')
    # commloss2017=nil.merge(jijel_data,on="COMMUNE",right_on = 'code', how = 'left')
    # print(commloss2017.head())

    #Read data to json.
    # merged_json = json.loads(commloss2017.to_json())
    #Convert to String like object.
    # json_data = json.dumps(merged_json)
    #Define function that returns json_data for year selected by user.
    # print(jijel_data[jijel_data['THRESHOLD'] )  
    def json_data(selectedYear):
        yr = selectedYear
        df_yr = algerie_data[algerie_data['ANNEE'] == yr]
        merged = algerie_geo.merge(df_yr, left_on = 'NAME_2', right_on ='SUBNATIONAL2', how = 'left')
        # merged.fillna('No data', inplace = True)
        merged_json = json.loads(merged.to_json())
        json_data = json.dumps(merged_json)
        return json_data

    #Input GeoJSON source that contains features for plotting.
    geosource = GeoJSONDataSource(geojson = json_data(2001))
    #Define a sequential multi-hue color palette.
    palette = brewer['YlOrRd'][8]
    #Reverse color order so that dark blue is highest obesity.
    palette = palette[::-1]
    #Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors.
    color_mapper = LinearColorMapper(palette = palette, low = 0, high = 400, nan_color = '#d9d9d9')
    #Define custom tick labels for color bar.
    tick_labels = {'0': '0', '5': '5', '10':'10', '25':'25','50': '50','75':'75'}

    #Add hover tool
    hover = HoverTool(tooltips = [('Commune','@NAME_2'),('PERTES HA', '@PERTE')])

    #Create color bar. 
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,
    border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)
    #Create figure object.
    p = figure(title = 'Pertes des forets en Ha', plot_height= 550,plot_width= 1000, tools = "pan,wheel_zoom,box_zoom,reset,tap,crosshair")
    tile_providers = get_provider(Vendors.CARTODBPOSITRON)
    p.add_tile(tile_providers)
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    #Add patch renderer to figure. 
    p.patches('xs','ys', source = geosource,fill_color = {'field' :'PERTE', 'transform' : color_mapper},
            line_color = 'black', line_width = 0.25, fill_alpha = 1)
    #Specify figure layout.
    p.add_layout(color_bar, 'below')
    p.add_tools(hover)
    # Define the callback function: update_plot
    def update_plot(attr, old, new):
        yr = slider.value
        new_data = json_data(yr)
        geosource.geojson = new_data
        p.title.text = 'Pertes des forets année : %d' %yr

    # Make a slider object: slider 
    slider = Slider(title = 'Année',start = 2001, end = 2018, step = 1, value = 2018)
    slider.on_change('value', update_plot)
    #Link selection

    # Make a column layout of widgetbox(slider) and plot, and add it to the current document
    layout = column(p,column(slider)) 
# p = vplot(s1, s2, s3)
 


    script , div = components(layout)
    return render(request,'projet/bokehMap.html', {'script':script, 'div':div})
         



def starters(request):

# output_file("tile.html")

    tile_provider = get_provider(CARTODBPOSITRON)

    # range bounds supplied in web mercator coordinates
    p = figure(x_range=(-2000000, 6000000), y_range=(-1000000, 7000000),
               x_axis_type="mercator", y_axis_type="mercator")
    p.add_tile(tile_provider)
    data = dict(x=list(range(10)))
    source = ColumnDataSource(data=data)
    source.selected.indices = [1, 2]
    columns = [TableColumn(field="x", title="X")]
    data_table = DataTable(source=source, columns=columns)

    save(data_table)
    script , div = components(p)
    return render(request,'projet/starters.html', {'script':script, 'div':div})
