from typing import Callable

import ee
import geopandas as gpd

from geersd import Sentinel2

def _add_ndvi(image):
    return image.addBands(
        image.expression(
            expression="(NIR - Red) / (NIR + Red)",
            map_={"NIR": image.select('B8'), "Red": image.select('B4')}
        ).rename('NDVI').float()
    )

def get_index(key: str) -> Callable | None:
    index_factory = {
        'ndvi': _add_ndvi
    }
    
    return index_factory.get(key.lower(), None)


def _load_shapefile(filename: str):
    gdf = gpd.read_file(filename, driver='ESRI Shapefile')
    
    if len(gdf) > 1:
        gdf = gdf.iloc[[0]]

    if gdf.crs != 4326:
        gdf.to_crs(4326, inplace=True)
    
    return gdf


def _load_ee_asset(filename: str) -> ee.FeatureCollection:
    return ee.FeatureCollection(filename)


def load_aoi(filename: str) -> ee.Geometry:
    
    if filename.endswith('.shp'):
        table = _load_shapefile(filename)
        return ee.FeatureCollection(table.__geo_interface__).geometry()
    return _load_ee_asset(filename).geometry()


def insert_dt_props(x) -> ee.Image:
    dt = ee.Image(x).date()
    return x.set(
        {
            'doy': dt.getRelative('day', 'year').add(1).int(),
            'year': dt.format('YYYY')
        }
    )


def process_s2(aoi: ee.Geometry, dependent: str, start: str, end: str, cloud: int):
    index = get_index(dependent)

    dataset = (
        Sentinel2
        .surface_reflectance()
        .filterBounds(aoi)
        .filterDate(start, end)
        .filterCloud(cloud)
        .map(insert_dt_props)
    )
    
    # if cloud greater than one
    if cloud > 1:
        dataset = dataset.applyCloudMask()
    
    if index is not None:
        dataset = dataset.map(index)
    
    return dataset