from typing import Callable, Dict, Any
import functools

import ee

from geersd import Sentinel2


from pcft.vector_operations import load_ee_asset, shp2fc

from pcft import landsat


def _add_ndvi(nir: str, red: str):
    return lambda image: image.addBands(
        image.expression(
            expression="(NIR - Red) / (NIR + Red)",
            map_={"NIR": image.select(nir), "Red": image.select(red)},
        )
        .rename("NDVI")
        .float()
    )


def get_index(key: str) -> Callable | None:
    index_factory = {"ndvi": _add_ndvi}

    return index_factory.get(key.lower(), None)


def process_colllection(dataset, aoi, start, end, dependent, cloud = -1):
    dataset = dataset.filterBounds(aoi).filterDate(start, end).map(insert_dt_props)
    index = get_index(dependent) # if returns none assume that we are using a spectral band

    if cloud > -1:
        dataset = dataset.filterClouds(cloud)
    
    if hasattr(dataset, 'applySaclingFactor'):
        dataset = dataset.applyScalingFactor()
    
    dataset = dataset.applyCloudMask()
    
    if hasattr(dataset, 'rename'):
        dataset = dataset.rename() # handle the standardization of the bands for landsat only
    
    if index is not None and isinstance(dataset, landsat.LandsatSR): # TODO check this logic
        dataset = dataset.map(_add_ndvi('SR_B5', 'SR_B4'))
    else:
        dataset = dataset.map(_add_ndvi('B8', 'B4'))

    return dataset.select(dependent)


def fetch_proc(sensor: str):
    factory = {
        'l8': functools.partial(process_colllection, landsat.Landsat8SR()),
        'l5': functools.partial(process_colllection, landsat.Landsat5SR()),
        'l7': functools.partial(process_colllection, landsat.Landsat7SR()),
        's2': functools.partial(process_colllection, Sentinel2.surface_reflectance())
    }
    return factory[sensor]

# need to check what datasets to use base off the start year and the end year
# upper bounds is 2012
# lower bounds is 1984

"""
to include land sat 5 the lower bound needs to be gte 1984 and the upper bounds needs to be
lte 2012

if start gte 1984
add l5
if end gte 2013 # which is the start date for l8 we want to add land sat 8
add l8 

"""


def process_landsat_time_series(aoi, start, end, dependent, cloud = -1):
    include_l5 = True if start >= 1984 else False
    include_l8 = True if end >= 2013 else False

    dataset = None
    if include_l5:
        l5 = fetch_proc['l5'](aoi, start, end, dependent, cloud)
        dataset = l5
    
    if include_l8:
        l8 = fetch_proc['l8'](aoi, start, end, dependent, cloud)

    if dataset is None:
        dataset = l8
    else:
        dataset = dataset.merge(dataset)

    return dataset


def process_sentinel2_time_series(aoi, start, end, dependent, cloud = -1):
    return



def load_aoi(filename: str) -> ee.Geometry:
    if filename.endswith(".shp"):
        return shp2fc(filename)
    return load_ee_asset(filename).geometry()


def insert_dt_props(x) -> ee.Image:
    dt = ee.Image(x).date()
    return x.set(
        {"doy": dt.getRelative("day", "year").add(1).int(), "year": dt.format("YYYY")}
    )


