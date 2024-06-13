import pytest


from pcft.image_processing import process_colllection, fetch_proc
from pcft import landsat as ls

from helpers import test_point_aoi


def test_l8_process_collection():
    l8_proc = process_colllection(
        dataset=ls.Landsat8SR(),
        aoi=test_point_aoi,
        start="2013",
        end="2018",
        dependent="NDVI",
        cloud=10,
    )
    l8_proc.first().getInfo()


def test_l5_process_collection():
    l5_proc = process_colllection(
        dataset=ls.Landsat5SR(),
        aoi=test_point_aoi,
        start="2005",
        end="2010",
        dependent="NDVI",
        cloud=10,
    )
    l5_proc.first().getInfo()


def test_l7_process_collection():
    l7_proc = process_colllection(
        dataset=ls.Landsat7SR(),
        aoi=test_point_aoi,
        start="2005",
        end="2010",
        dependent="NDVI",
        cloud=10,
    )
    l7_proc.first().getInfo()


def test_fetch_proc():
    sensor = "l8"
    l8_proc = fetch_proc(sensor=sensor)(
        aoi=test_point_aoi, start="2013", end="2018", dependent="NDVI", cloud=10
    )
    l8_proc.first().getInfo()


def test_fetch_invalid_proc():
    with pytest.raises(KeyError):
        fetch_proc(sensor="Invalid")
