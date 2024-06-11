import ee
import geopandas as gpd


def load_shapefile(filename: str):
    gdf = gpd.read_file(filename, driver="ESRI Shapefile")

    if len(gdf) > 1:
        gdf = gdf.iloc[[0]]

    if gdf.crs != 4326:
        gdf.to_crs(4326, inplace=True)

    return gdf


def shp2fc(filename: str) -> ee.Geometry:
    """loads and converts a shapefile to feature collection"""
    return ee.FeatureCollection(load_shapefile(filename).__geo_interface__).geometry()


def load_ee_asset(filename: str) -> ee.FeatureCollection:
    """loads the asset and grabs the geometry of the first feature"""
    return ee.FeatureCollection(filename).first().geometry()
