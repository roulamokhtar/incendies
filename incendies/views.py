# Create your views here.
from django.shortcuts import render, redirect ,get_list_or_404, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, TemplateView, DetailView, DeleteView
from django.urls import reverse_lazy
from .models import *
from .forms import  IncendieForm , InterventionForm  ,TypeFormationincendieForm,MoyenForm,DegatForm
from django.forms import modelformset_factory , inlineformset_factory
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.core import serializers  
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.template import loader
from django.core.paginator import Paginator
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_gis.filters import InBBoxFilter
# from .serializers import AdSerializer,AdCommuneSerializer
from django.contrib.gis.geos import GEOSGeometry,Polygon
from django.db import connection
from django.contrib.gis.db.models.functions import Intersection  
from django.db.models.functions import Coalesce
from django.db.models import Subquery,OuterRef,Sum,Count,Max,Value as V ,FloatField, F
from django.db import connection
from django.db.models import F
from bokeh.palettes import Category20c,Category20,Dark2,Plasma
from bokeh.transform import cumsum
from math import pi
import decimal
import json
import time
import csv
import pandas as pd
from bokeh.plotting import ColumnDataSource, figure, output_file, show
from bokeh.embed import components
from bokeh.models import Slider, HoverTool, GeoJSONDataSource,ColumnDataSource,LassoSelectTool,WheelZoomTool,Circle,Line,Rect,Text,Plot,LinearColorMapper,ColorBar
from bokeh.models.tools import HoverTool
from bokeh.palettes import Spectral6,Spectral10
from bokeh.tile_providers import CARTODBPOSITRON, get_provider,Vendors
 
from bokeh.palettes import brewer
from bokeh.layouts import widgetbox, row, column
import os
import json
import simplejson
import math
import datetime

 # Create your views here.
# class InterventionDeleteView(DeleteView):
# 	model = Intervention
	# success_url = reverse_lazy('detail ')
 	 
def remove_intervention(request,incendie_id, intervention_id):
	Incendie.objects.get(id = incendie_id).intervention_set.get(id = intervention_id).delete()  
	return redirect('detail', incendie_id=incendie_id)

def remove_materiel(request,incendie_id, moyen_id):
	Incendie.objects.get(id = incendie_id).moyen_set.get(id = moyen_id).delete()  
	return redirect('detail', incendie_id=incendie_id)

def remove_typeformationincendie(request,incendie_id, typeformationincendie_id):
	Incendie.objects.get(id = incendie_id).typeformationincendie_set.get(id = typeformationincendie_id).delete()  
	return redirect('detail', incendie_id=incendie_id)

def remove_degat(request,incendie_id, degat_id):
	Incendie.objects.get(id = incendie_id).degat_set.get(id = degat_id).delete()  
	return redirect('detail', incendie_id=incendie_id)

class InterventionUpdateView(UpdateView):
	model = Intervention
	form_class = InterventionForm

class MoyenUpdateView(UpdateView):
	model = Moyen
	form_class = MoyenForm

class TypeFormationincendieView(UpdateView):
	model = TypeFormationincendie
	form_class = TypeFormationincendieForm

class DegatView(UpdateView):
	model = Degat
	form_class = DegatForm


class IncendieCreate(LoginRequiredMixin,CreateView):
	model = Incendie
	form_class = IncendieForm
	def get_form(self, form_class=None):
		form = super().get_form(form_class)
		form.fields['wilaya'].queryset = Wilaya.objects.filter(user= self.request.user)
		return form
	def form_valid(self, form):
		#assign the logged in user (self.request.user)
		form.instance.user = self.request.user
		# Let the  CreateView do  its job  as usual
		return super().form_valid(form)
@login_required	 
def index(request):
 	return render(request,'incendies/about.html')

def incendies_index(request):
	if request.user.username == 'DGF':
 		incendies = Incendie.objects.all()
	else:
		incendies = Incendie.objects.filter(user= request.user)
	return render(request, 'incendies/incendie_list.html', {'incendies':incendies})

def incendies_detail(request,incendie_id):
	incendie = Incendie.objects.get(id=incendie_id)
	intervention_form = InterventionForm()
	TypeFormationincendie_Form = TypeFormationincendieForm()
	Moyen_Form = MoyenForm()
	Degat_Form = DegatForm()

	return render(request, 'incendies/incendie_detail.html', {
		'incendie':incendie,
		'intervention_form':intervention_form,
 		'TypeFormationincendie_Form':TypeFormationincendie_Form,
 		'Moyen_Form':Moyen_Form,
 		'Degat_Form':Degat_Form
		})
def add_intervention(request, incendie_id):
	#create a modelform using the data  in the request.POST
	form = InterventionForm(request.POST)
	# VALID THE FORM
	if form.is_valid():
		new_intervention = form.save(commit=False)
		new_intervention.incendie_id = incendie_id
		new_intervention.save()
	return redirect('detail', incendie_id=incendie_id)

def add_typeFormationincendie(request, incendie_id):
	#create a modelform using the data  in the request.POST
	form = TypeFormationincendieForm(request.POST)
	# VALID THE FORM
	if form.is_valid():
		new_typeFormationincendie = form.save(commit=False)
		new_typeFormationincendie.incendie_id = incendie_id
		new_typeFormationincendie.save()
	return redirect('detail', incendie_id=incendie_id)
def add_Moyen(request, incendie_id):
	#create a modelform using the data  in the request.POST
	form = MoyenForm(request.POST)
	# VALID THE FORM
	if form.is_valid():
		new_moyenForm = form.save(commit=False)
		new_moyenForm.incendie_id = incendie_id
		new_moyenForm.save()
	return redirect('detail', incendie_id=incendie_id)
def add_Degat(request, incendie_id):
	#create a modelform using the data  in the request.POST
	form = DegatForm(request.POST)
	# VALID THE FORM
	if form.is_valid():
		new_degat = form.save(commit=False)
		new_degat.incendie_id = incendie_id
		new_degat.save()
	return redirect('detail', incendie_id=incendie_id)

def cartofeux(request):
    # canton =  Canton.objects.filter(layer__contains='FD')
    # communes =  Limite_commune.objects.all()
    # perimetres =  Perimetre.objects.all()
    # beneficiares = Parcellaire_perimetre.objects.all()
    # foret_recreatives = Foret_recreative.objects.all()
    # reboisements = Reboisement.objects.filter(kml_folder__contains='Programme 2017')
 
    return render(request,'incendies/layoutmap.html')
    # ,{
    # 'Canton':canton,
    # 'communes':communes,
    # 'perimetres':perimetres,
    # 'beneficiares':beneficiares,
    # 'foret_recreatives':foret_recreatives,
    # 'reboisements':reboisements,
   
    # } 
    
# def localites(request):
#     localites = serialize('geojson', Localites.objects.all())
#     return HttpResponse(localites,content_type='json')
# def brigade(request):
#     brigade = serialize('geojson', Brigade.objects.all())
#     return HttpResponse(brigade,content_type='json')

def feux(request):
    # feux =  Incendie.objects.filter(intervention__moyensMobilise =4)
    x=  simplejson.dumps([a.get_json() for a in Incendie.objects.all()],default=str) 
    return HttpResponse(x,content_type='json')
 
def synthese(request):
	start_date = None
	 

	if request.user.username == 'DGF':
		nombreFoyer =   Wilaya.objects.exclude(name = 'DGF').annotate(dcount=Coalesce(Count('incendie__lieudit'),0)).order_by('-dcount','name') 
		nombreFoyer= nombreFoyer.values('name','dcount')

		superficie = Wilaya.objects.exclude(name = 'DGF').annotate(superficie=Coalesce(Sum('incendie__typeformationincendie__sup'),0)).order_by('-superficie','name')
		superficie= superficie.values('name','superficie')

		superficieTotal = Incendie.objects.aggregate(superficie_total=Coalesce(Sum('typeformationincendie__sup'),0))
		superficieEncours = Incendie.objects.filter(dateExt= start_date).aggregate(superficie_encours=Coalesce(Sum('typeformationincendie__sup'),0))
		superficieMairise = Incendie.objects.exclude(dateExt = start_date).aggregate(superficie_maitrise=Coalesce(Sum('typeformationincendie__sup'),0))

		nombreFoyerTotal = Incendie.objects.aggregate(nombre_total=Coalesce(Count('id'),0))
		nombreFoyerEncours = Incendie.objects.filter(dateExt= start_date).aggregate(nombre_encours=Coalesce(Count('id'),0))
		nombreFoyerMairise = Incendie.objects.exclude(dateExt = start_date).aggregate(nombre_maitrise=Coalesce(Count('id'),0))

		sup_juin = Incendie.objects.filter(dateDepart__range=["2020-06-01", "2020-06-30"]).aggregate(superficie_total=Coalesce(Sum('typeformationincendie__sup'),0))
		sup_juil= Incendie.objects.filter(dateDepart__range=["2020-07-01", "2020-07-31"]).aggregate(superficie_total=Coalesce(Sum('typeformationincendie__sup'),0))
		sup_aout = Incendie.objects.filter(dateDepart__range=["2020-08-01", "2020-07-31"]).aggregate(superficie_total=Coalesce(Sum('typeformationincendie__sup'),0))
		sup_sept= Incendie.objects.filter(dateDepart__range=["2020-09-01", "2020-09-30"]).aggregate(superficie_total=Coalesce(Sum('typeformationincendie__sup'),0))

		nbr_juin = Incendie.objects.filter(dateDepart__range=["2020-06-01", "2020-06-30"]).aggregate(nombre=Coalesce(Count('id'),0))
		nbr_juil= Incendie.objects.filter(dateDepart__range=["2020-07-01", "2020-07-31"]).aggregate(nombre=Coalesce(Count('id'),0))
		nbr_aout = Incendie.objects.filter(dateDepart__range=["2020-08-01", "2020-07-31"]).aggregate(nombre=Coalesce(Count('id'),0))
		nbr_sept= Incendie.objects.filter(dateDepart__range=["2020-09-01", "2020-09-30"]).aggregate(nombre=Coalesce(Count('id'),0))
		# superficiemois = Incendie.objects.aggregate(superficie_total=Sum('typeformationincendie__sup'))
		superficieformation = Typeformation.objects.annotate(superficie=Coalesce(Sum('typeformationincendie__sup'),0)).order_by('-superficie','name')
		superficieformation= superficieformation.values('name','superficie')

		all_incendie_types = Incendie.objects.values('typeformationincendie__typeformation__name').exclude(typeformationincendie__sup=None).annotate(superficie_formation=Sum('typeformationincendie__sup'))
		sum_incendie_types = Incendie.objects.all().aggregate(sum_superficie = Sum('typeformationincendie__sup'))
		dict_of_percentages = { superficie['typeformationincendie__typeformation__name']:superficie['superficie_formation'] * 100/ sum_incendie_types['sum_superficie']
		for superficie in all_incendie_types }

		all_incendie_typesespece = Incendie.objects.values('typeformationincendie__espece__name').exclude(typeformationincendie__sup=None).annotate(superficie_formation=Sum('typeformationincendie__sup'))
		sum_incendie_typesespece = Incendie.objects.all().aggregate(sum_superficie = Sum('typeformationincendie__sup'))
		dict_of_percentages_espece = { superficie['typeformationincendie__espece__name']:superficie['superficie_formation'] * 100/ sum_incendie_types['sum_superficie']
		for superficie in all_incendie_typesespece }
	else:
		nombreFoyer = Commune.objects.filter(wilaya__name= request.user.username).annotate(dcount=Coalesce(Count('incendie__lieudit'),0)).order_by('-dcount','name')
		nombreFoyer= nombreFoyer.values('name','dcount')

		superficie = Commune.objects.filter(wilaya__name= request.user.username).annotate(superficie=Coalesce(Sum('incendie__typeformationincendie__sup'),0)).order_by('-superficie','name')
		superficie= superficie.values('name','superficie')


		superficieTotal = Incendie.objects.filter(wilaya__name= request.user.username).aggregate(superficie_total=Coalesce(Sum('typeformationincendie__sup'),0))
		superficieEncours = Incendie.objects.filter(dateExt= start_date,wilaya__name= request.user.username).aggregate(superficie_encours=Coalesce(Sum('typeformationincendie__sup'),0))
		superficieMairise = Incendie.objects.exclude(dateExt = start_date).filter(wilaya__name= request.user.username).aggregate(superficie_maitrise=Coalesce(Sum('typeformationincendie__sup'),0))

		nombreFoyerTotal = Incendie.objects.filter(wilaya__name= request.user.username).aggregate(nombre_total=Coalesce(Count('id'),0))
		nombreFoyerEncours = Incendie.objects.filter(dateExt= start_date , wilaya__name= request.user.username).aggregate(nombre_encours=Coalesce(Count('id'),0))
		nombreFoyerMairise = Incendie.objects.exclude(dateExt = start_date).filter(wilaya__name= request.user.username).aggregate(nombre_maitrise=Coalesce(Count('id'),0))
		sup_juin = Incendie.objects.filter(dateDepart__range=["2020-06-01", "2020-06-30"],wilaya__name= request.user.username).aggregate(superficie_total=Coalesce(Sum('typeformationincendie__sup'),0))
		sup_juil= Incendie.objects.filter(dateDepart__range=["2020-07-01", "2020-07-31"],wilaya__name= request.user.username).aggregate(superficie_total=Coalesce(Sum('typeformationincendie__sup'),0))
		sup_aout = Incendie.objects.filter(dateDepart__range=["2020-08-01", "2020-07-31"],wilaya__name= request.user.username).aggregate(superficie_total=Coalesce(Sum('typeformationincendie__sup'),0))
		sup_sept= Incendie.objects.filter(dateDepart__range=["2020-09-01", "2020-09-30"],wilaya__name= request.user.username).aggregate(superficie_total=Coalesce(Sum('typeformationincendie__sup'),0))
		nbr_juin = Incendie.objects.filter(dateDepart__range=["2020-06-01", "2020-06-30"],wilaya__name= request.user.username).aggregate(nombre=Coalesce(Count('id'),0))
		nbr_juil= Incendie.objects.filter(dateDepart__range=["2020-07-01", "2020-07-31"],wilaya__name= request.user.username).aggregate(nombre=Coalesce(Count('id'),0))
		nbr_aout = Incendie.objects.filter(dateDepart__range=["2020-08-01", "2020-07-31"],wilaya__name= request.user.username).aggregate(nombre=Coalesce(Count('id'),0))
		nbr_sept= Incendie.objects.filter(dateDepart__range=["2020-09-01", "2020-09-30"],wilaya__name= request.user.username).aggregate(nombre=Coalesce(Count('id'),0))

		superficieformation = Typeformation.objects.filter(typeformationincendie__incendie__wilaya__name= request.user.username).annotate(superficie=Coalesce(Sum('typeformationincendie__sup'),0)).order_by('-superficie','name')
		superficieformation= superficieformation.values('name','superficie')

		all_incendie_types = Incendie.objects.filter(wilaya__name= request.user.username).values('typeformationincendie__typeformation__name').exclude(typeformationincendie__sup=None).annotate(superficie_formation=Coalesce(Sum('typeformationincendie__sup'),0))
		sum_incendie_types = Incendie.objects.filter(wilaya__name= request.user.username).aggregate(sum_superficie = Sum('typeformationincendie__sup'))
		dict_of_percentages = { superficie['typeformationincendie__typeformation__name']:superficie['superficie_formation'] * 100/ sum_incendie_types['sum_superficie']
		for superficie in all_incendie_types }
		print(all_incendie_types)

		all_incendie_typesespece = Incendie.objects.filter(wilaya__name= request.user.username).values('typeformationincendie__espece__name').exclude(typeformationincendie__sup=None).annotate(superficie_formation=Coalesce(Sum('typeformationincendie__sup'),0))
		sum_incendie_typesespece = Incendie.objects.filter(wilaya__name= request.user.username).aggregate(sum_superficie = Sum('typeformationincendie__sup'))
		dict_of_percentages_espece = { superficie['typeformationincendie__espece__name']:superficie['superficie_formation'] * 100/ sum_incendie_types['sum_superficie']
		for superficie in all_incendie_typesespece }


		 


	return render(request,'incendies/syntheseDGF.html',{
		'nombrefoyer':nombreFoyer,
		'superficie':superficie,
		'superficieTotal':superficieTotal,
		'superficieEncours':superficieEncours,
		'superficieMairise':superficieMairise,
		'nombreFoyerTotal':nombreFoyerTotal,
		'nombreFoyerEncours':nombreFoyerEncours,
		'nombreFoyerMairise':nombreFoyerMairise,
		'sup_juin' :sup_juin ,
		'sup_juil' : sup_juil,
		'sup_aout'  :sup_aout ,
		'sup_sept' :  sup_sept,
		'nbr_juin':nbr_juin,
		'nbr_juil':nbr_juil,
		'nbr_aout':nbr_aout,
		'nbr_sept':nbr_sept,
		'superficieformation':superficieformation,
		'dict_of_percentages':dict_of_percentages,
		'dict_of_percentages_espece':dict_of_percentages_espece
 

	})
	 
	

class IncendieUpdateView(LoginRequiredMixin,UpdateView):
	model = Incendie
	form_class = IncendieForm
	 
  
class IncendieDeleteView(LoginRequiredMixin,DeleteView):
    model = Incendie
    form_class = IncendieForm
    success_url = reverse_lazy('incendies_index')

def load_communes(request):
    wilaya_id = request.GET.get('wilaya')
    xx = Commune.objects.filter(wilaya_id=wilaya_id).order_by('name')
    return render(request, 'incendies/commune_dropdown_list_options.html', {'communes': xx})
# def load_wilayas(request):
#     user_id = request.GET.get('user')
#     wilayas = Wilaya.objects.filter(user_id=user_id).order_by('name')
    # return render(request, 'incendies/wilaya_dropdown_list_options.html', {'wilayas': wilayas})

def graph(request):
	if request.user.username == 'DGF':
		queryset = User.objects.annotate(dcount=Coalesce(Count('incendie__lieudit'),0)).exclude(username ='DGF')
		superficie = Incendie.objects.annotate(superficie=Sum('typeformationincendie__sup'))
	else:
		queryset = Commune.objects.filter(wilaya__name= request.user.username).annotate(dcount=Count('incendie__lieudit'))
		superficie = Commune.objects.annotate(superficie=Coalesce(Sum('incendie__typeformationincendie__sup'),V(0))).filter(wilaya__name= request.user.username)
	return render(request,'incendies/graphBokeh.html')

def nombrefoyergraph(request):
	shows = 0
	counts = []
	items = []
	sup =[]
	supetatfeux =[]
	itemsuperficie =[]
	itemsuperficieencoursmaitrise =[]
	start_date = datetime.datetime(2020, 6, 1 , 00 , 00, 00)  


	if request.user.username == 'DGF':
		nombreFoyer =   Wilaya.objects.exclude(name = 'DGF').annotate(dcount=Coalesce(Count('incendie__lieudit'),0)).order_by('-dcount') 
		nombreFoyer= nombreFoyer.values('name','dcount')

		superficiecommune = Wilaya.objects.exclude(name = 'DGF').annotate(superficie=Coalesce(Sum('incendie__typeformationincendie__sup'),0)).order_by('-superficie')
		superficiecommune= superficiecommune.values('name','superficie')

		superficieTotal = Incendie.objects.aggregate(superficie_total=Coalesce(Sum('typeformationincendie__sup'),0))
		nombreFoyerTotal = Incendie.objects.aggregate(nombre_total=Coalesce(Count('id'),0))


		all_incendie_typesespece = Incendie.objects.values('typeformationincendie__espece__name').exclude(typeformationincendie__sup=None).annotate(superficie_formation=Sum('typeformationincendie__sup'))
		sum_incendie_types = Incendie.objects.aggregate(sum_superficie = Sum('typeformationincendie__sup'))
		dict_of_percentages_espece = { superficie['typeformationincendie__espece__name']:superficie['superficie_formation'] * 100/ sum_incendie_types['sum_superficie']
		for superficie in all_incendie_typesespece }

		all_incendie_type_formation = Incendie.objects.values('typeformationincendie__typeformation__name').exclude(typeformationincendie__sup=None).annotate(superficie_formation=Sum('typeformationincendie__sup'))
		sum_incendie_types_formation = Incendie.objects.aggregate(sum_superficie = Sum('typeformationincendie__sup'))
		dict_of_percentages_type_formation = { superficie['typeformationincendie__typeformation__name']:superficie['superficie_formation'] * 100/ sum_incendie_types_formation['sum_superficie']
		for superficie in all_incendie_type_formation }


	else:
		nombreFoyer = Commune.objects.filter(wilaya__name= request.user.username).annotate(dcount=Count('incendie__lieudit')).order_by('-dcount')
		nombreFoyer= nombreFoyer.values('name','dcount')

		superficiecommune = Commune.objects.filter(wilaya__name= request.user.username).annotate(superficie=Sum('incendie__typeformationincendie__sup')).order_by('superficie')
		superficiecommune= superficiecommune.values('name','superficie')

		nombreFoyerTotal = Incendie.objects.filter(wilaya__name= request.user.username).aggregate(nombre_total=Coalesce(Count('id'),0))
		superficieTotal = Incendie.objects.filter(wilaya__name= request.user.username).aggregate(superficie_total=Coalesce(Sum('typeformationincendie__sup'),0))

		all_incendie_typesespece = Incendie.objects.filter(wilaya__name= request.user.username).exclude(typeformationincendie__sup=None).values('typeformationincendie__espece__name').annotate(superficie_formation=Sum('typeformationincendie__sup'))
		sum_incendie_types = Incendie.objects.filter(wilaya__name= request.user.username).aggregate(sum_superficie = Sum('typeformationincendie__sup'))
		dict_of_percentages_espece = { superficie['typeformationincendie__espece__name']:superficie['superficie_formation'] * 100/ sum_incendie_types['sum_superficie']
		for superficie in all_incendie_typesespece }

		all_incendie_type_formation = Incendie.objects.filter(wilaya__name= request.user.username).exclude(typeformationincendie__sup=None).values('typeformationincendie__typeformation__name').annotate(superficie_formation=Sum('typeformationincendie__sup'))
		sum_incendie_types_formation = Incendie.objects.aggregate(sum_superficie = Sum('typeformationincendie__sup'))
		dict_of_percentages_type_formation = { superficie['typeformationincendie__typeformation__name']:superficie['superficie_formation'] * 100/ sum_incendie_types_formation['sum_superficie']
		for superficie in all_incendie_type_formation }
#################################################################################################################################
		# cas ou il ya au minimum un feux ett une superficie renseigné

	if(nombreFoyerTotal['nombre_total'] !=0 and superficieTotal['superficie_total'] !=0):
		print(' nombreFoyer' ,nombreFoyerTotal)

		print(' superficieTotal',superficieTotal)

		print(' nombreFoyer et superficieTotal >0')
		for sd in nombreFoyer:
			counts.append(sd['dcount'])
			print(counts)
			items.append(sd["name"])
			items = list(map(str, items))
			plotNombre = figure(x_range= items,plot_height= 400,plot_width= 1000, title="Nombre de Foyer",toolbar_location = "right", tools = "pan,wheel_zoom,box_zoom,reset,tap,crosshair",y_range=(0, max(counts)))
			source = ColumnDataSource(data = dict(xx=items, zz=counts, color=Spectral6))
			plotNombre.vbar(x='xx',top='zz', width=.5, color ='color',source = source)
			plotNombre.xaxis.major_label_orientation = math.pi/2

		hover = HoverTool()
		hover.tooltips="""
		<div>
		<h5>@xx</h3>
		<div><strong>Nombre de foyer:</strong>@zz</div>
		</div>
		"""

		plotNombre.add_tools(hover)


 
		###################################################################################################################################
		for i in superficiecommune:
			sup.append(i['superficie'])
			itemsuperficie.append(i["name"])
			itemsuperficie = list(map(str, itemsuperficie))
			plotsuperficie = figure(x_range= itemsuperficie,plot_height= 400,plot_width= 1000, title="Superficie de feux ",toolbar_location = "right", tools = "pan,wheel_zoom,box_zoom,reset,tap,crosshair")
			source1 = ColumnDataSource(data = dict(aa=itemsuperficie, bb=sup, color=Spectral6))
			plotsuperficie.vbar(x='aa',top='bb', width=.5, color ='color',source = source1)
			plotsuperficie.xaxis.major_label_orientation = math.pi/2

			# gestion du hover
		hover2 = HoverTool()
		hover2.tooltips="""
		<div>
		<h5>@aa</h5>
		<div><strong>Superficie des incendies:</strong>@bb Ha</div>
		</div>
		"""


		plotsuperficie.add_tools(hover2)

		hover3 = HoverTool()
		hover3.tooltips="""
		<div>
		<h5>@ff</h5>
		<div><strong>Superficie des incendies:</strong>@gg </div>
		</div>
		"""



	

###################################################################################################################################
		dataPercentages_espece = pd.DataFrame.from_dict(dict(dict_of_percentages_espece), orient='index').reset_index()
		dataPercentages_espece = dataPercentages_espece.rename(index=str, columns={0:'value', 'index':'country'})

		dataPercentages_espece['angle'] = dataPercentages_espece['value']/sum(dict_of_percentages_espece.values()) * 2* decimal.Decimal(pi)

			  # partie de gestion des couleurs dans l'histogramme par  especes

		if (len(dict_of_percentages_espece) == 2):
			print('salut 2')
			dataPercentages_espece['color'] =('#440154', '#30678D')
		elif(len(dict_of_percentages_espece) == 1):
			print('salut 1')
			dataPercentages_espece['color'] =('#440154')
		else:
			print('salut plus que 2')
			dataPercentages_espece['color'] = Category20[len(dict_of_percentages_espece )]

		p_incendie_espece = figure(plot_height=350,plot_width=450, title="Taux d'incendie par espèce", toolbar_location=None,
			tools="hover", tooltips=[("Espèce", "@country"),("Pourcentage", "@value %")])

		p_incendie_espece.wedge(x=0, y=1, radius=0.4, 
			start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
			line_color="white", fill_color='color', legend='country', source=data)

		p_incendie_espece.axis.axis_label=None
		p_incendie_espece.axis.visible=False
		p_incendie_espece.grid.grid_line_color = None
	################################################################
	 			# partie de gestion des pourcentage % par  type de formation

		data = pd.DataFrame.from_dict(dict(dict_of_percentages_type_formation), orient='index').reset_index()
		data = data.rename(index=str, columns={0:'value', 'index':'country'})
	 
		data['angle'] = data['value']/sum(dict_of_percentages_type_formation.values()) * 2* decimal.Decimal(pi)

			# gestion des couleurs selon le cas
		if (len(dict_of_percentages_type_formation) == 2):
			print('salut 2')
			data['color'] =('#440154', '#30678D')
		elif(len(dict_of_percentages_type_formation) == 1):
			print('salut 1')
			data['color'] =('#440154')
		else:
			print('salut plus que 2')
			data['color'] = Category20[len(dict_of_percentages_type_formation )] 

		p_incendie_type_formation = figure(plot_height=350,plot_width=450, title="Taux d'incendie par Type de formation forestière", toolbar_location=None,
			tools="hover", tooltips=[("Espèce", "@country"),("Pourcentage", "@value %")])

		p_incendie_type_formation.wedge(x=0, y=1, radius=0.4, 
			start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
			line_color="white", fill_color='color', legend='country', source=data)

		p_incendie_type_formation.axis.axis_label=None
		p_incendie_type_formation.axis.visible=False
		p_incendie_type_formation.grid.grid_line_color = None
	


################################################################""

		layout = column(plotNombre,column(plotsuperficie),row(children=[p_incendie_espece, p_incendie_type_formation], sizing_mode='stretch_both'),divRemarque) 
		# p = vplot(s1, s2, s3)

		script, div = components(layout)	 
	elif(nombreFoyerTotal['nombre_total'] !=0 and superficieTotal['superficie_total'] ==0):
		print('nombreFoyer>0 et superficieTotal ==0 ')

		for sd in nombreFoyer:
			counts.append(sd['dcount'])
			print(counts)
			items.append(sd["name"])
			items = list(map(str, items))
			plotNombre = figure(x_range= items,plot_height= 400,plot_width= 1000, title="Nombre de Foyer",toolbar_location = "right", tools = "pan,wheel_zoom,box_zoom,reset,tap,crosshair",y_range=(0, max(counts)))
			source = ColumnDataSource(data = dict(xx=items, zz=counts, color=Spectral6))
			plotNombre.vbar(x='xx',top='zz', width=.5, color ='color',source = source)
			plotNombre.xaxis.major_label_orientation = math.pi/2

		hover = HoverTool()
		hover.tooltips="""
		<div>
		<h5>@xx</h3>
		<div><strong>Nombre de foyer:</strong>@zz</div>
		</div>
		"""

		plotNombre.add_tools(hover)

		div2 =     '<div class="center-align">' "<span style = 'color:red'  >" 'Pas de superficie renseigné dans votre wilaya' "</span>" '</div>'

		layout = column(plotNombre) 
	 
		script, div = components(layout)	 
	else:
		print('nombreFoyer==0 et superficieTotal ==0 ')
 

		div =     '<div class="center-align">' "<span style = 'color:red'  >" 'Pas dincendies dans votre wilaya' "</span>" '</div>'
		script = ''
 
	return render (request, 'incendies/graphBokeh.html', {'script':script, 'div':div,'div2':div2})

def algerie(request):
	wilaya = serialize('geojson', Wilaya.objects.filter(user= request.user))
	return HttpResponse(wilaya,content_type='json')
# def Pourcentage(request):
# 	pourcentage = serialize('geojson', Typeformation.objects.filter(typeformationincendie__incendie__wilaya__user= request.user).annotate(pourcent = Sum('typeformationincendie__sup')))
# 	return HttpResponse(pourcentage,content_type='json')
def Pourcentage(request):
	# all_incendie_types = Incendie.objects.all().values('lieudit')
	# num_incendie_types = len(all_incendie_types)

	# dict_of_percentages = { lieudit['lieudit']:lieudit['lieudit__count'] * 100/num_incendie_types
	# for lieudit in all_incendie_types.annotate(Count('lieudit')) }

	all_incendie_types = Incendie.objects.values('typeformationincendie__typeformation__name').annotate(superficie_formation=Sum('typeformationincendie__sup'))
	print(all_incendie_types)
	# {'typeformationincendie__sup': Decimal('2.00')}{'typeformationincendie__sup': Decimal('4.00')}{'typeformationincendie__sup': Decimal('7.00')}
	sum_incendie_types = Incendie.objects.all().aggregate(sum_superficie = Sum('typeformationincendie__sup'))
	# print(sum_incendie_types)
	#3

	dict_of_percentages = { superficie['typeformationincendie__typeformation__name']:superficie['superficie_formation'] * 100/ sum_incendie_types['sum_superficie']
	for superficie in all_incendie_types }
	# print (dict_of_percentages)
	return HttpResponse(dict_of_percentages,content_type='json')

def load_especes(request):
    typeformation_id = request.GET.get('typeformation')
    especes = Espece.objects.filter(typeformation_id=typeformation_id).order_by('name')
    return render(request, 'incendies/espece_dropdown_list_options.html', {'especes': especes})

def signup(request):
    error_message =''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # this is how we index 
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

def limite_commune(request):
    limite_communes = serialize('geojson', Limite_commune.objects.all())
    return HttpResponse(limite_communes,content_type='json')
def localites(request):
    localites = serialize('geojson', Localites.objects.all())
    return HttpResponse(localites,content_type='json')

 