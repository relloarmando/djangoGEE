# generic base view
from django.views.generic import TemplateView


# folium
import folium
from folium.plugins import MousePosition
from folium import plugins

# gee
import ee

ee.Initialize()

# Add custom basemaps to folium
basemaps = {
    'Google Maps': folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Maps',
        overlay = True,
        control = True
    ),
    'Google Satellite': folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Satellite',
        overlay = True,
        control = True
    ),
    'Google Terrain': folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Terrain',
        overlay = True,
        control = True
    ),
    'Google Satellite Hybrid': folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Satellite',
        overlay = True,
        control = True
    ),
    'Esri Satellite': folium.TileLayer(
        tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr = 'Esri',
        name = 'Esri Satellite',
        overlay = True,
        control = True
    )
}

gdl = {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [
              -102.78259277343749,
              20.545525954214707
            ],
            [
              -102.7140998840332,
              20.54536521151087
            ],
            [
              -102.7027702331543,
              20.56513529562339
            ],
            [
              -102.75100708007811,
              20.583938610571174
            ],
            [
              -102.78671264648438,
              20.567867545031778
            ],
            [
              -102.78259277343749,
              20.545525954214707
            ]
          ]
        ]
      }
}

# home
class home(TemplateView):
    template_name = 'index.html'

    # Define a method for displaying Earth Engine image tiles on a folium map.
    def get_context_data(self, **kwargs):
        figure = folium.Figure()

        # create Folium Object
        mapObj = folium.Map(
            location=[20.47, -103],
            zoom_start=8
        )

        folium.GeoJson(gdl, name='polygon').add_to(mapObj)
        basemaps['Google Satellite Hybrid'].add_to(mapObj)
        folium.LatLngPopup().add_to(mapObj)

        # add map to figure
        mapObj.add_to(figure)

        # select the Dataset Here's used the MODIS data
        dataset = (ee.ImageCollection('MODIS/006/MOD13Q1')
                   .filter(ee.Filter.date('2021-07-01', '2021-11-30'))
                   .first())
        modisndvi = dataset.select('NDVI')
        modisevi = dataset.select('EVI')
        # Styling
        vis_paramsNDVI = {
            'min': 0,
            'max': 8000,
            'palette': [ 'FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163', '99B718', '74A901',
                '66A000', '529400', '3E8601', '207401', '056201', '004C00', '023B01',
                '012E01', '011D01', '011301' ]}


        # add the map to the the folium map
        map_id_dict = ee.Image(modisndvi).getMapId(vis_paramsNDVI)
        map_id_dict2 = ee.Image(modisevi).getMapId(vis_paramsNDVI)

        # GEE raster data to TileLayer
        folium.raster_layers.TileLayer(
            tiles=map_id_dict['tile_fetcher'].url_format,
            attr='Google Earth Engine',
            name='NDVI',
            overlay=True,
            control=True
        ).add_to(mapObj)

        folium.raster_layers.TileLayer(
            tiles=map_id_dict2['tile_fetcher'].url_format,
            attr='Google Earth Engine',
            name='EVI',
            overlay=True,
            control=True
        ).add_to(mapObj)

        # add Layer control
        mapObj.add_child(folium.LayerControl())

        # figure
        figure.render()

        # return map
        return {"map": figure}