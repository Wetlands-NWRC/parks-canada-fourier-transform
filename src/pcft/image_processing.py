from typing import Callable
import functools

import ee
from geersd import Sentinel2
from pcft import landsat


def insert_dt_props(x) -> ee.Image:
    dt = ee.Image(x).date()
    return x.set(
        {"doy": dt.getRelative("day", "year").add(1).int(), "year": dt.format("YYYY")}
    )


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


def process_colllection(dataset, aoi, start, end, dependent, cloud=-1):
    dataset = dataset.filterBounds(aoi).filterDate(start, end).map(insert_dt_props)
    index = get_index(
        dependent
    )  # if returns none assume that we are using a spectral band

    if cloud > -1:
        if hasattr(dataset, "filterCloud"):  # to statisfy symantic dif in S2 class
            dataset = dataset.filterCloud(cloud)
        else:
            dataset = dataset.filterClouds(cloud)

    if hasattr(dataset, "applyScalingFactor"):
        dataset = dataset.applyScalingFactor()

    dataset = dataset.applyCloudMask()

    if hasattr(dataset, "rename"):
        dataset = (
            dataset.rename()
        )  # handle the standardization of the bands for landsat only

    if index is not None and isinstance(
        dataset, landsat.LandsatSR
    ):  # TODO check this logic
        dataset = dataset.map(_add_ndvi("SR_B5", "SR_B4"))
    else:
        dataset = dataset.map(_add_ndvi("B8", "B4"))

    return dataset.select(dependent)


def fetch_proc(sensor: str):
    factory = {
        "l8": functools.partial(process_colllection, landsat.Landsat8SR()),
        "l5": functools.partial(process_colllection, landsat.Landsat5SR()),
        "l7": functools.partial(process_colllection, landsat.Landsat7SR()),
        "s2": functools.partial(process_colllection, Sentinel2.surface_reflectance()),
    }
    return factory[sensor]
