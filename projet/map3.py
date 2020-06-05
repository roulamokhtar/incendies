import os
import csv
import pandas as pd
import geopandas as gpd
from bokeh.plotting import ColumnDataSource, figure, output_file, show
from bokeh.embed import components
from bokeh.models import Slider, HoverTool,Div,CustomJS,Select, GeoJSONDataSource,ColumnDataSource,LassoSelectTool,WheelZoomTool,Circle,Line,Rect,Text,Plot,LinearColorMapper,ColorBar
from bokeh.models.tools import HoverTool
from bokeh.palettes import Spectral6
from bokeh.tile_providers import CARTODBPOSITRON, get_provider,Vendors
from bokeh.io import output_notebook, show, output_file,curdoc
from bokeh.palettes import brewer
from bokeh.layouts import widgetbox, row, column   
import branca.colormap as cm
import json
from bokeh.io import curdoc, output_notebook
from bokeh.models import Slider, HoverTool,TapTool
from bokeh.layouts import widgetbox, row, column

#Define function that returns json_data for year selected by user.
    
algerie = os.path.join('data', 'gadm_jijel.geojson')
algerie_geo = gpd.read_file(algerie)
algerie_geo=algerie_geo[['NAME_1','NAME_2','geometry']]
loss_algerie = os.path.join('data','loss_jijel_10.csv')
algerie_data = pd.read_csv(loss_algerie,encoding="ISO-8859-1")
#Define function that returns json_data for year selected by user.
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
# char = ColumnDataSource(data=dict(x=json_data.SUBNATIONAL2, y=json_data.PERTE))
   
 
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
p = figure(title = 'Pertes des forets en Ha', plot_height= 550,plot_width= 800, tools = "pan,wheel_zoom,box_zoom,reset,tap,crosshair")
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
 
########################################
# Create the ColumnDataSource object "s1"
# s1 = ColumnDataSource(data=dict(x = algerie_data['SUBNATIONAL2'],y=algerie_data['PERTE']))
# p1 = figure(x_range= algerie_data['SUBNATIONAL2'],plot_height= 550,plot_width= 1200, title=p.title.text,toolbar_location = "below", tools = "pan,wheel_zoom,box_zoom,reset,tap,crosshair" )

# source = ColumnDataSource(data = dict(x=algerie_data['SUBNATIONAL2'], y=algerie_data['PERTE'], color=Spectral6))
# p.add_tools(LassoSelectTool())
# p.add_tools(WheelZoomTool())
def json_data_chart(selectedYear):
    yr = selectedYear
    df_yr = algerie_data[algerie_data['ANNEE'] == yr]
    # merged = algerie_geo.merge(df_yr, left_on = 'NAME_2', right_on ='SUBNATIONAL2', how = 'left')
    # merged.fillna('No data', inplace = True)
    # merged_json = json.loads(df_yr.to_json())
    # json_data_chart = json.dumps(merged_json)
    return df_yr


 

x_bar = json_data_chart(2011)
y_bar = json_data_chart(2011)

xx =x_bar['SUBNATIONAL2']
print(xx)
yy =y_bar['PERTE']
print(yy)
json_data_chart(2001).head()
s1 = ColumnDataSource(json_data_chart(2001))

#Input  JSON source that contains features for plotting.
p1 = figure(x_range= s1.data['SUBNATIONAL2'],plot_height= 550,plot_width= 550,
 toolbar_location = "below", tools = "pan,wheel_zoom,box_zoom,reset,tap,crosshair" )
 
p1.yaxis.axis_label = 'Superficie en Ha'
p1.xaxis.major_label_orientation = "vertical"
p1.vbar(x='SUBNATIONAL2',top='PERTE', width=.8, source = s1)
hover1 = HoverTool(tooltips = [('Commune','@SUBNATIONAL2'),('PERTES HA', '@PERTE')])

p1.add_tools(hover1)
# Create the figure object "p1"
# p1 = figure(title='Click on a column to display more information',
#             plot_width=500, plot_height=325, x_range = x_bar,
#             toolbar_location=None, tools=['hover', 'tap'], tooltips='@$PERTE')

# p1.vbar( x='x_bar',top=y_bar, width=.5)
# Add stacked vertical bars to "p1"
 # Change parameters of "p1"
# p1.title.align = 'center'
# p1.xaxis.axis_label = 'Lifeboat (in launch order)'
# p1.yaxis.axis_label = 'Count'
p1.y_range.start = 0
p1.x_range.range_padding = 0.05
p1.xgrid.grid_line_color = None
# p1.legend.orientation = 'horizontal'
# p1.legend.location = 'top_left'

def update_plot_chart(attr, old, new):
    yr = slider.value
    new_data_chart = json_data_chart(yr)
    s1.data = new_data_chart
    p1.title.text = 'Pertes des forets année : %d' %yr
# Create the Div object "div1"
div1 = Div()

# Create the custom JavaScript callback
callback1 = CustomJS(args=dict(s1=s1, div1=div1), code='''
    var ind = s1.selected.indices;
    if (String(ind) != '') {
        lifeboat = s1.data['ANNEE'][ind];
        female = s1.data['PERTE'][ind];
        male = s1.data['SUBNATIONAL2'][ind];
        message = '<b>Lifeboat: ' + String(lifeboat) +  '</b><br>Females: ' + String(female) +  '<br>Males: ' + String(male) +  '<br>Total: ' + String(female+male);
        div1.text = message;
    }
    else {
        div1.text = '';
    }
    ''') 
    # When tapping the plot "p1" execute the "callback1"
p1.js_on_event('tap', callback1)

#################################
# Make a slider object: slider 
slider = Slider(title = 'Année',start = 2001, end = 2018, step = 1, value = 2018)
slider.on_change('value', update_plot,update_plot_chart)
#Link selection
 
# Make a column layout of widgetbox(slider) and plot, and add it to the current document
layout = column(
    row(p,p1),
    row(slider,column(div1)),
 )

curdoc().add_root(layout)

