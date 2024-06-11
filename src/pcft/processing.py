from typing import Callable, Dict, Any

import ee
import geopandas as gpd


class Lansat8Sr(ee.ImageCollection):
    def __init__(self):
        super().__init__("LANDSAT/LC08/C02/T1_L2")

    def filterBounds(self, geometry: Dict[str, Any] | ee.Geometry) -> ee.Any:
        return self.filter(ee.Filter.bounds(geometry))

    def filterDate(self, start, end):
        return self.filter(ee.Filter.date(start, end))

    def filterClouds(self, percent: float):
        return self.filter(ee.Filter.lte("CLOUD_COVER", percent))

    def applyCloudMask(self):
        return self.map(self.cloud_mask)

    @staticmethod
    def cloud_mask(image):
        """mask clouds and applies scaling factor"""
        qaMask = image.select("QA_PIXEL").bitwiseAnd(int("11111", 2)).eq(0)
        saturationMask = image.select("QA_RADSAT").eq(0)
        opticalBands = image.select("SR_B.").multiply(0.0000275).add(-0.2)
        thermalBands = image.select("ST_B.*").multiply(0.00341802).add(149.0)
        return (
            image.addBands(opticalBands, None, True)
            .addBands(thermalBands, None, True)
            .updateMask(qaMask)
            .updateMask(saturationMask)
        )


def _add_ndvi(image):
    return image.addBands(
        image.expression(
            expression="(NIR - Red) / (NIR + Red)",
            map_={"NIR": image.select("SR_B5"), "Red": image.select("SR_B4")},
        )
        .rename("NDVI")
        .float()
    )


def get_index(key: str) -> Callable | None:
    index_factory = {"ndvi": _add_ndvi}

    return index_factory.get(key.lower(), None)


def _load_shapefile(filename: str):
    gdf = gpd.read_file(filename, driver="ESRI Shapefile")

    if len(gdf) > 1:
        gdf = gdf.iloc[[0]]

    if gdf.crs != 4326:
        gdf.to_crs(4326, inplace=True)

    return gdf


def _load_ee_asset(filename: str) -> ee.FeatureCollection:
    return ee.FeatureCollection(filename)


def load_aoi(filename: str) -> ee.Geometry:

    if filename.endswith(".shp"):
        table = _load_shapefile(filename)
        return ee.FeatureCollection(table.__geo_interface__).geometry()
    return _load_ee_asset(filename).geometry()


def insert_dt_props(x) -> ee.Image:
    dt = ee.Image(x).date()
    return x.set(
        {"doy": dt.getRelative("day", "year").add(1).int(), "year": dt.format("YYYY")}
    )


def process_l8(aoi: ee.Geometry, dependent: str, start: str, end: str, cloud: int):
    """processing chain for landsat 8 sr"""
    index = get_index(dependent)

    dataset = (
        Lansat8Sr()
        .filterBounds(aoi)
        .filterDate(start, end)
        .filterClouds(cloud)
        .map(insert_dt_props)
    )

    # if cloud greater than one
    if cloud > 1:
        dataset = dataset.applyCloudMask()

    if index is not None:
        dataset = dataset.map(index)

    return dataset
