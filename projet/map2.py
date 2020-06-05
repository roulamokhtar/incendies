  
import os
import time
import requests
import csv
# from projet import integration
# from projet import example_noteBook
# from projet.integration import *
# from projet.integration import m
# import ee
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
     
import branca.colormap as cm

import json

 
import datetime

from folium.folium import Map

from IPython.display import HTML

from bokeh.io import curdoc, output_notebook
from bokeh.models import Slider, HoverTool,TapTool
from bokeh.layouts import widgetbox, row, column
#Define function that returns json_data for year selected by user.
    
algerie = os.path.join('data', 'gadm36_dza_2.geojson')
    # fname = 'NILZone.shp'
algerie_geo = gpd.read_file(algerie)
algerie_geo=algerie_geo[['NAME_1','NAME_2','geometry']]
# print(nil.head())
loss_algerie = os.path.join('data','loss_algeria_10.csv')
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
color_mapper = LinearColorMapper(palette = palette, low = 0, high = 300, nan_color = '#d9d9d9')
#Define custom tick labels for color bar.
tick_labels = {'0': '0', '5': '5', '10':'10', '25':'25','50': '50','75':'75'}

#Add hover tool
hover = HoverTool(tooltips = [ ('Wilaya','@NAME_1'),('Commune','@NAME_2'),('PERTES HA', '@PERTE')])

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

# Make a column layout of widgetbox(slider) and plot, and add it to the current document
layout = column(p,column(slider))
curdoc().add_root(layout)
    
# Make a slider object: slider 
	# slider = Slider(title = 'Year',start = 1975, end = 2016, step = 1, value = 2016)
	# slider.on_change('value', update_plot)
	# Make a column layout of widgetbox(slider) and plot, and add it to the current document





######################################

#############################################################################
# import os
# import folium
# import geopandas as gpd
# import matplotlib
# assert 'naturalearth_lowres' in gpd.datasets.available
# datapath = gpd.datasets.get_path('naturalearth_lowres')
# gdf = gpd.read_file(datapath)
# # %matplotlib inline
# # print(gdf.head(5))
# import pandas as pd


# n_periods, n_sample = 48, 40

# assert n_sample < n_periods

# datetime_index = pd.date_range('2016-1-1', periods=n_periods, freq='M')
# dt_index_epochs = datetime_index.astype(int) // 10**9
# dt_index = dt_index_epochs.astype('U10')

# # print(dt_index)
# import numpy as np


# styledata = {}

# for country in gdf.index:
#     df = pd.DataFrame(
#         {'color': np.random.normal(size=n_periods),
#          'opacity': np.random.normal(size=n_periods)},
#         index=dt_index
#     )
#     df = df.cumsum()
#     df.sample(n_sample, replace=False).sort_index()
#     styledata[country] = df
#     # print(gdf.loc[0])
#     # print(styledata.get(0).head())

#     ax = df.plot()
#     max_color, min_color, max_opacity, min_opacity = 0, 0, 0, 0

# for country, data in styledata.items():
#     max_color = max(max_color, data['color'].max())
#     min_color = min(max_color, data['color'].min())
#     max_opacity = max(max_color, data['opacity'].max())
#     max_opacity = min(max_color, data['opacity'].max())

#     from branca.colormap import linear


# cmap = linear.PuRd_09.scale(min_color, max_color)


# def norm(x):
#     return (x - x.min()) / (x.max() - x.min())


# for country, data in styledata.items():
#     data['color'] = data['color'].apply(cmap)
#     data['opacity'] = norm(data['opacity'])

# print(styledata.get(0).head())

# styledict = {
#     str(country): data.to_dict(orient='index') for
#     country, data in styledata.items()
# }

# from folium.plugins import TimeSliderChoropleth

# m = folium.Map([0, 0], tiles='Stamen Toner', zoom_start=2)

# g = TimeSliderChoropleth(
#     gdf.to_json(),
#     styledict=styledict,

# ).add_to(m)
# m.save('templates/projet/mapJijel2010.html')

# m.save(os.path.join('results', 'TimeSliderChoropleth.html'))

# m
###################################################################################################
# import folium

# import ipyleaflet
# import ipywidgets
# from ipywidgets.embed import embed_minimal_html

# from ipyleaflet import basemaps, Map
# from ipywidgets import IntSlider

# # basic_map = ipyleaflet.Map(zoom=1)

# # m = folium.Map(
	 
# # 	location= [36.69789, 5.90438],
# # 	zoom_start = 10,
# # 	) 
 
# # display map
# # basic_map
# radio_button = ipywidgets.RadioButtons(options=['Positron', 'DarkMatter', 'WorldStreetMap', 'DeLorme', 
#                                                 'WorldTopoMap', 'WorldImagery', 'NatGeoWorldMap', 'HikeBike', 
#                                                 'HyddaFull', 'Night', 'ModisTerra', 'Mapnik', 'HOT', 'OpenTopoMap', 
#                                                 'Toner', 'Watercolor'],
#                                        value='Positron', 
#                                        description='map types:')

# def toggle_maps(map):
#     if map == 'Positron': m = Map(zoom=2, basemap=basemaps.CartoDB.Positron)
#     if map == 'DarkMatter': m = Map(zoom=1, basemap=basemaps.CartoDB.DarkMatter)
#     if map == 'WorldStreetMap': m = Map(center=(40.67, -73.94), zoom=10, basemap=basemaps.Esri.WorldStreetMap)
#     if map == 'DeLorme': m = Map(center=(40, -99), zoom=4, basemap=basemaps.Esri.DeLorme)
#     if map == 'WorldTopoMap': m = Map(center=(40, -99), zoom=4, basemap=basemaps.Esri.WorldTopoMap)
#     if map == 'WorldImagery': m = Map(center=(40, -99), zoom=4, basemap=basemaps.Esri.WorldImagery)
#     if map == 'NatGeoWorldMap': m = Map(center=(40, -99), zoom=4, basemap=basemaps.Esri.NatGeoWorldMap)
#     if map == 'HikeBike': m = Map(center=(39.73, -104.98), zoom=10, basemap=basemaps.HikeBike.HikeBike)
#     if map == 'HyddaFull': m = Map(center=(40, -99), zoom=4, basemap=basemaps.Hydda.Full)
#     if map == 'Night': m = Map(center=(40, -99), zoom=4, basemap=basemaps.NASAGIBS.ViirsEarthAtNight2012)
#     if map == 'ModisTerra': m = Map(center=(40, -99), zoom=4, basemap=basemaps.NASAGIBS.ModisTerraTrueColorCR)
#     if map == 'Mapnik': m = Map(center=(40, -99), zoom=4, basemap=basemaps.OpenStreetMap.Mapnik)
#     if map == 'HOT': m = Map(center=(40, -99), zoom=4, basemap=basemaps.OpenStreetMap.HOT)
#     if map == 'OpenTopoMap': m = Map(center=(40, -99), zoom=4, basemap=basemaps.OpenTopoMap)
#     if map == 'Toner': m = Map(center=(40, -99), zoom=4, basemap=basemaps.Stamen.Toner)
#     if map == 'Watercolor': m = Map(center=(40, -99), zoom=4, basemap=basemaps.Stamen.Watercolor)
#     display(m)
        
# ipywidgets.interact(toggle_maps, map=radio_button)
# ipyleaflet.s
# # m.save('templates/projet/mapJijel2010.html')
# slider = IntSlider(value=40)

# embed_minimal_html('templates/projet/mapJijel2010.html', views=[slider], title='Widgets export')
