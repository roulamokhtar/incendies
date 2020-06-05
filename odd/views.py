from django.shortcuts import render, redirect ,get_list_or_404, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.http import HttpResponse,JsonResponse
from django.template import loader
# from .serializers import AdSerializer,AdCommuneSerializer
from django.contrib.gis.geos import GEOSGeometry,Polygon
from django.db import connection
import json
import time
import requests
import csv
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

@login_required
def mapJijel2010(request):
    return render(request,'projet/mapJijel2010.html')


def odd15(request):
    return render(request,'odd/odd15.html')

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
    zz = []
    xx = []

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
