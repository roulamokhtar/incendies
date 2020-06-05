import ee
import folium
from eeconvert import eeImageToFoliumLayer as ee_plot
import webbrowser
# import ee.mapclient
import math
import datetime
import sys

from folium.folium import Map
from ipyleaflet import Map, VideoOverlay

from IPython.display import HTML,Image
import matplotlib.pyplot as plt

try:
	ee.Initialize()
	print('The Earth Engine package initialized successfuly!')

except ee.EEExeption as e:
	print('The Earth Engine package failed to initialized')
except:
	print("Unexpected error :", sys.exc_info()[0])
	raise
 # //Load and filter the Hansen data
# srtm = ee.Image('srtm90_v4')
# srtm = srtm.visualize(min=300, max=2500)
# def inline_map(m):
#     if isinstance(m, Map):
#         m._build_map()
#         srcdoc = m.HTML.replace('"', '&quot;')
#         embed = HTML('<iframe srcdoc="{srcdoc}" '
#                      'style="width: 100%; height: 500px; '
#                      'border: none"></iframe>'.format(srcdoc=srcdoc))
#     else:
#         raise ValueError('{!r} is not a folium Map instance.')
#     return embed
url_base = 'http://services.arcgisonline.com/arcgis/rest/services/'
service = 'World_Imagery/MapServer/tile/{z}/{y}/{x}'
tileset = url_base + service
# Link to Esri World Imagery service plus attribution
EsriImagery = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
EsriAttribution = "Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community"
# MapObject = folium.Map(location=[64.9865, -18.5867], tiles=EsriImagery, attr=EsriAttribution, zoom_start=7)

m = folium.Map(
	 
	location= [36.69789, 5.90438],
	zoom_start = 10,
	tiles =  EsriImagery,

	attr=EsriAttribution 
	) 


 
 
# width, height = 650, 450
 # m = Map(width=width, height=height, location=[36.69789, 5.90438], zoom_start=10)
# add = '/MapServer/tile/{z}/{y}/{x}'

# ESRI = dict(World_Ocean_Base='http://services.arcgisonline.com/arcgis/rest/services/Ocean/World_Ocean_Base',
#             World_Navigation_Charts='http://services.arcgisonline.com/ArcGIS/rest/services/Specialty/World_Navigation_Charts',
#             World_Ocean_Reference='http://services.arcgisonline.com/arcgis/rest/services/Ocean/World_Ocean_Reference',
#             NatGeo_World_Map='http://services.arcgisonline.com/arcgis/rest/services/NatGeo_World_Map/MapServer',
#             World_Imagery='http://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer',
#             World_Physical_Map='http://services.arcgisonline.com/arcgis/rest/services/World_Physical_Map/MapServer',
#             World_Shaded_Relief='http://services.arcgisonline.com/arcgis/rest/services/World_Shaded_Relief/MapServer',
#             World_Street_Map='http://services.arcgisonline.com/arcgis/rest/services/World_Street_Map/MapServer',
#             World_Terrain_Base='http://services.arcgisonline.com/arcgis/rest/services/World_Terrain_Base/MapServer',
#             World_Topo_Map='http://services.arcgisonline.com/arcgis/rest/services/World_Topo_Map/MapServer')
# Add the USGS style tile
#             World_Imagery='http://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer',


# for tile_name, tile_url in ESRI.items():
#     tile_url += add
#     m.add_tile_layer(tile_name=tile_name,\
#     				tile_url=tile_url)
# m.add_layers_to_map()
# inline_map(m)

# distr = ee.FeatureCollection('ft:1v6E4xgs_utdWFEFe5_VzBzAWOcRvGLuuCBEhWWZA','geometry') 
distr = ee.FeatureCollection("users/raoulmokh/communes_jijel");
hansen = ee.Image('UMD/hansen/global_forest_change_2018_v1_6').clipToCollection(distr);
# 
forest = hansen.select(['treecover2000']);
forest = forest.mask(forest);
lossYear = hansen.select(['lossyear']);
mask_annees =lossYear.gte(10);
lossGlobal = hansen.select(['loss']);
lossGlobal = lossGlobal.updateMask(lossGlobal);
gain = hansen.select(['gain']);
gain = gain.updateMask(gain);
######################################################
lossInYear9 = lossYear.eq(9).rename('2009');
lossInYear9 = lossInYear9.updateMask(lossInYear9);

lossInYear10 = lossYear.eq(10).rename('2010');
lossInYear10 = lossInYear10.updateMask(lossInYear10);

lossInYear11 = lossYear.eq(11).rename('2011');
lossInYear11 = lossInYear11.updateMask(lossInYear11);

lossInYear12 = lossYear.eq(12).rename('2012');
lossInYear12 = lossInYear12.updateMask(lossInYear12);

lossInYear13 = lossYear.eq(13).rename('2013');
lossInYear13 = lossInYear13.updateMask(lossInYear13);

lossInYear14 = lossYear.eq(14).rename('2014');
lossInYear14 = lossInYear14.updateMask(lossInYear14);

lossInYear15 = lossYear.eq(15).rename('2015');
lossInYear15 = lossInYear15.updateMask(lossInYear15);

lossInYear16 = lossYear.eq(16).rename('2016');
lossInYear16 = lossInYear16.updateMask(lossInYear16);

lossInYear17 = lossYear.eq(17).rename('2017');
lossInYear17 = lossInYear17.updateMask(lossInYear17);

lossInYear18 = lossYear.eq(18).rename('2018');
lossInYear18 = lossInYear18.updateMask(lossInYear18);
forest_cover_2000 = hansen.select(['treecover2000']).mask(forest).rename('Masktreecover2000');
lossInSevenYear = lossYear.gte(1).And(lossYear.lte(17));
losstAt2006 = forest.where(lossInSevenYear.eq(1), 0).rename('ddddd');

vis = {
    'min': 0,
    'max': 1,
    'palette': [
        'FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163',
        '99B718', '74A901', '66A000', '529400', '3E8601',
        '207401', '056201', '004C00', '023B01', '012E01',
        '011D01', '011301'
    ]}
vis_params = {
   
  'max': 100,
  'palette': ['000000', '00FF00']}

vis_params_perte = {
  'min': 0,
  'max': 1,
  'palette': ['FF0000']}

  

def add_ee_layer(self, ee_image_object, vis_params, name):
  map_id_dict = ee.Image(ee_image_object).getMapId(vis_params)
  folium.raster_layers.TileLayer(
    tiles = map_id_dict['tile_fetcher'].url_format,
    attr = "Map Data © Google Earth Engine",
    name = name,
    overlay = True,
    control = True
  ).add_to(self)
 # Add EE drawing method to folium.
 #################################################################################

def Radians(img):
  return img.toFloat().multiply(math.pi).divide(180)




def Hillshade(az, ze, slope, aspect):
  """Compute hillshade for the given illumination az, el."""
  azimuth = Radians(ee.Image(az))
  zenith = Radians(ee.Image(ze))
  # Hillshade = cos(Azimuth - Aspect) * sin(Slope) * sin(Zenith) +
  #     cos(Zenith) * cos(Slope)
  return (azimuth.subtract(aspect).cos()
          .multiply(slope.sin())
          .multiply(zenith.sin())
          .add(
              zenith.cos().multiply(slope.cos())))
 #################################################################################
# terrain = ee.Algorithms.Terrain(ee.Image('CGIAR/SRTM90_V4'))
# slope_img = Radians(terrain.select('slope'))
# aspect_img = Radians(terrain.select('aspect'))
# ee.mapclient.addToMap(Hillshade(0, 60, slope_img, aspect_img))

 #################################################################################
folium.Map.add_ee_layer = add_ee_layer

# feature_group1 = folium.FeatureGroup(name = 'Hansen 2017')
# feature_group2 = folium.FeatureGroup(name = 'Perte 2011-2017')
# feature_group3 = folium.FeatureGroup(name = 'sssssssssssssss')
m.add_ee_layer(forest,vis_params,'forêt 2000')
m.add_ee_layer(losstAt2006,vis_params,'forêt 2017')
m.add_ee_layer(lossGlobal,vis_params_perte,'Pertes 2000-2017')
m.add_ee_layer(lossInYear9,vis_params_perte,'Pertes 2009')
m.add_ee_layer(lossInYear10,vis_params_perte,'Pertes 2010')
m.add_ee_layer(lossInYear11,vis_params_perte,'Pertes 2011')
m.add_ee_layer(lossInYear12,vis_params_perte,'Pertes 2012')
m.add_ee_layer(lossInYear13,vis_params_perte,'Pertes 2013')
m.add_ee_layer(lossInYear14,vis_params_perte,'Pertes 2014')
m.add_ee_layer(lossInYear15,vis_params_perte,'Pertes 2015')
m.add_ee_layer(lossInYear16,vis_params_perte,'Pertes 2016')
m.add_ee_layer(lossInYear17,vis_params_perte,'Pertes 2017')
m.add_ee_layer(lossInYear18,vis_params_perte,'Pertes 2018') 
 




########################"ECoREGION"##########################
# # Load a FeatureCollection from a table dataset: 'RESOLVE' ecoregions.
# ecoregions = ee.FeatureCollection('RESOLVE/ECOREGIONS/2017')

# # Display as default and with a custom color.
# # m.add_child(ecoregions)
# # m.add_child(ecoregions, {'color': 'FF0000'}, 'colored')


 

# # Create an empty image into which to paint the features, cast to byte.
# empty = ee.Image().byte()

# # Paint all the polygon edges with the same number and 'width', display.
# outline = empty.paint(**{
#   'featureCollection': ecoregions,
#   'color': 1,
#   'width': 3
# })
# m.add_ee_layer(outline, {'palette': 'FF0000'}, 'edges')

##########################FIN ECIREGION########

dataset = ee.Image('JRC/GSW1_0/GlobalSurfaceWater').clipToCollection(distr)
occurrence = dataset.select('occurrence');
occurrenceVis = {'min': 0.0, 'max': 100.0, 'palette': ['0000ff']}
m.add_ee_layer(occurrence, occurrenceVis, 'Occurrence')
#####################################################################
# img = (ee.ImageCollection("COPERNICUS/S2_SR")
# 			.filterDate(datetime.datetime(2019, 4, 1),
# 	                          datetime.datetime(2019, 7, 1))
# 	              .filterBounds(distr))
img2019 = (ee.ImageCollection("COPERNICUS/S2_SR")
			.filterDate(datetime.datetime(2019, 1, 1),
	                          datetime.datetime(2019, 11, 30)))
# img2018 = (ee.ImageCollection("COPERNICUS/S2_SR")
# 			.filterDate(datetime.datetime(2018, 1, 1),
# 	                          datetime.datetime(2018, 12, 31)))
img2017 = (ee.ImageCollection("COPERNICUS/S2_SR")
			.filterDate(datetime.datetime(2017, 1, 1),
	                          datetime.datetime(2017, 12, 31)))
img2016 = (ee.ImageCollection("COPERNICUS/S2")
			.filterDate(datetime.datetime(2016, 1, 1),
	                          datetime.datetime(2016, 12, 31)))
##########################################################

# image1 = img.median()
image2019 = img2019.median() 
# image2018 = img2018.median() 
image2017 = img2017.median() 
image2016 = img2016.median()
################################
image2019 = image2019.clipToCollection(distr)
# image2018 = image2018.clipToCollection(distr)
image2017 = image2017.clipToCollection(distr)
image2016 = image2016.clipToCollection(distr)

#####################################
ndvi2019 = image2019.normalizedDifference(['B8','B4'])
# ndvi2018 = image2018.normalizedDifference(['B8','B4'])
ndvi2017 = image2017.normalizedDifference(['B8','B4'])
ndvi2016 = image2016.normalizedDifference(['B8','B4'])

# swr = img2.select(['B12','B8','B5'])
pal = ["red","yellow","green"]
pal2 = ["red","green","blue"]
# swir = image2.select('B12', 'B8', 'B5')
vis_swir = {
  'min':0,
  'max': 1,
   
  }
 
m.add_ee_layer(ndvi2019,{'min':0,'max':1,'palette':pal},'NDVI jijel 2019')
m.add_ee_layer(ndvi2017,{'min':0,'max':1,'palette':pal},'NDVI jijel 2017')
m.add_ee_layer(ndvi2016,{'min':0,'max':1,'palette':pal},'NDVI jijel 2016')

# m.add_ee_layer(swir,vis_swir,'swir jijel 2019')
# m.add_ee_layer(swr,{'min':500,'max':3300,'palette':pal},'swr jijel 2018')
###############################################################################################
imgLandsat2019 = (ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA")
			.filterDate(datetime.datetime(2019, 1, 1),
	                          datetime.datetime(2019, 11, 30)))
imgLandsat2018 = (ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA")
			.filterDate(datetime.datetime(2018, 1, 1),
	                          datetime.datetime(2018, 12, 31)))
imgLandsat2017 = (ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA")
			.filterDate(datetime.datetime(2017, 1, 1),
	                          datetime.datetime(2017, 12, 31)))



imgLandsat2019 = imgLandsat2019.min() 
imgLandsat2019 = imgLandsat2019.clipToCollection(distr)

imgLandsat2018 = imgLandsat2018.min() 
imgLandsat2018 = imgLandsat2018.clipToCollection(distr)

imgLandsat2017 = imgLandsat2017.min() 
imgLandsat2017 = imgLandsat2017.clipToCollection(distr)



 

# # Create an NDWI image, define visualization parameters and display.
ndwi2019 = imgLandsat2019.normalizedDifference(['B3', 'B5'])
ndwi2018 = imgLandsat2018.normalizedDifference(['B3', 'B5'])
ndwi2017 = imgLandsat2017.normalizedDifference(['B3', 'B5'])
ndwiViz = {'min': 0.5, 'max': 1, 'palette': ['00FFFF', '0000FF']}

# # Mask the non-watery parts of the image, where NDWI < 0.4.
ndwiMasked2019 = ndwi2019.updateMask(ndwi2019.gte(0.4))
ndwiMasked2018 = ndwi2018.updateMask(ndwi2018.gte(0.4))
ndwiMasked2017 = ndwi2017.updateMask(ndwi2017.gte(0.4))
# Map.addLayer(ndwi, ndwiViz, 'NDWI', False)
 
m.add_ee_layer(ndwiMasked2019, ndwiViz, 'NDWI masked 2019')
m.add_ee_layer(ndwiMasked2018, ndwiViz, 'NDWI masked 2018')
m.add_ee_layer(ndwiMasked2017, ndwiViz, 'NDWI masked 2017')

 
 
# 
m.add_child(folium.map.LayerControl()) 


m.save('projet/templates/projet/hansen.html')

 
# Fetch a Landsat image.
# img = ee.Image('LANDSAT/LT05/C01/T1_SR/LT05_034033_20000913')

# # Select Red and NIR bands, scale them, and sample 500 points.
# samp_fc = img.select(['B3','B4']).divide(10000).sample(scale=30, numPixels=500)

# # Arrange the sample as a list of lists.
# samp_dict = samp_fc.reduceColumns(ee.Reducer.toList().repeat(2), ['B3', 'B4'])
# samp_list = ee.List(samp_dict.get('list'))

# # Save server-side ee.List as a client-side Python list.
# samp_data = samp_list.getInfo()

# # Display a scatter plot of Red-NIR sample pairs using matplotlib.
# plt.scatter(samp_data[0], samp_data[1], alpha=0.2)
# plt.xlabel('Red', fontsize=12)
# plt.ylabel('NIR', fontsize=12)
# plt.show()
##############################
# elev = ee.Image('CGIAR/SRTM90_V4').clipToCollection(distr)
# cover = ee.Image('MODIS/051/MCD12Q1/2001_01_01').select('Land_Cover_Type_1')
# blank = ee.Image(0)


# # Where (1 <= cover <= 4) and (elev > 1000), set the output to 1.
# output = blank.where(
#     cover.lte(4).And(cover.gte(1)).And(elev.gt(1000)),
#     1)


# # Output contains 0s and 1s.  Mask it with itself to get rid of the 0s.
# result = output.mask(output)
# # m.add_ee_layer(result,{'palette': '00AA00'},'forest classes above 1000m')
#############################
if __name__ == '__main__':
    try:
        arg = sys.argv[1]
    except IndexError:
        arg = None

    return_val = add_ee_layer(arg)

