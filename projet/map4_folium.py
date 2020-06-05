# this example works fine
import pandas as pd
import geopandas as gpd
import folium
# import branca.colormap as cm
import os

jijel = os.path.join('data', 'gadm36_dza_2.geojson')

# fname = 'NILZone.shp'
nil = gpd.read_file(jijel)
nil.crs = "EPSG:4326"    # set it by hand

nil=nil[['NAME_1','NAME_2','geometry']]
# print(nil.head())
loss_jijel = os.path.join('data','loss_algeria_10.csv')
jijel_data = pd.read_csv(loss_jijel,encoding="ISO-8859-1")
# jijel_data['NAME_2']=jijel_data['SUBNATIONAL2']
jijel_data = jijel_data[jijel_data['ANNEE']==2018]
# jijel_data=jijel_data[['NAME_2','SUBNATIONAL1','ANNEE','SUBNATIONAL2','PERTE']]
# print(jijel_data.head())
commloss2017=nil.merge(jijel_data,left_on = 'NAME_2', right_on ='SUBNATIONAL2', how = 'left')
# commloss2017 = nil.merge(df_yr, left_on = 'NAME_2', right_on ='SUBNATIONAL2', how = 'left')

print(commloss2017.head())

x_map=nil.centroid.x.mean()
y_map=nil.centroid.y.mean()
print(x_map,y_map)

mymap = folium.Map(location=[y_map, x_map], zoom_start=11,tiles=None)
folium.TileLayer().add_to(mymap)

myscale = (commloss2017['PERTE'].quantile((0,0.1,0.75,0.9,0.98,1))).tolist()
folium.Choropleth(
 geo_data=commloss2017,
 name='Pertes 2018',
 data=commloss2017,
 columns=['NAME_2','PERTE'],
 key_on="feature.properties.NAME_2",
 fill_color='YlOrRd',
 threshold_scale=myscale,
 fill_opacity=1,
 line_opacity=0.2,
 legend_name='Pertes des forets année 2018 en Ha',
 highlight=True
).add_to(mymap)

style_function = lambda x: {'fillColor': '#ffffff', 
                            'color':'#000000', 
                            'fillOpacity': 0.1, 
                            'weight': 0.1}
highlight_function = lambda x: {'fillColor': '#000000', 
                                'color':'#000000', 
                                'fillOpacity': 0.50, 
                                'weight': 0.1}
NIL = folium.features.GeoJson(
    commloss2017,
    style_function=style_function, 
    control=False,
    highlight_function=highlight_function, 
    tooltip=folium.features.GeoJsonTooltip(
        fields=['NAME_1','NAME_2','PERTE'],
        aliases=['Wiaya:','Commune: ','Pertes en Ha: '],
        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
    )
)
mymap.add_child(NIL)
mymap.keep_in_front(NIL)
folium.LayerControl().add_to(mymap)
mymap.save('templates/projet/mapJijel2010.html')