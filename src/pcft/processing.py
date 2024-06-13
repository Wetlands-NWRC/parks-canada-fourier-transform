from pcft.vector_operations import load_aoi
from pcft.image_processing import fetch_proc


def process_landsat_time_series(aoi, start, end, dependent, cloud=-1):
    aoi = load_aoi(aoi)
    include_l5 = int(start) < 2012
    include_l8 = int(end) >= 2013 

    dataset = None
    if include_l5:
        l5 = fetch_proc("l5")(aoi, start, end, dependent, cloud)
        dataset = l5

    if include_l8:
        l8 = fetch_proc("l8")(aoi, start, end, dependent, cloud)
        
        if dataset is not None:
            dataset = dataset.merge(l8)
        else:
            dataset = l8

    return dataset


def process_sentinel2_time_series(aoi, start, end, dependent, cloud=-1):
    aoi = load_aoi(aoi)
    return fetch_proc["s2"](aoi, start, end, dependent, cloud)
