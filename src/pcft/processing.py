from pcft.vector_operations import load_aoi
from pcft.image_processing import fetch_proc


def process_landsat_time_series(aoi, start, end, dependent, cloud = -1):
    aoi = load_aoi(aoi)
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
    aoi = load_aoi(aoi)
    return  fetch_proc['s2'](aoi, start, end, dependent, cloud)
