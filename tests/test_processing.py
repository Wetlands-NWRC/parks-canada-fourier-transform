from pcft import processing as proc


asset_id = "users/ryangilberthamilton/bq-trend-analysis/subset_BoQ_for_Ken_v2"


def test_landsat_workflow_include_only_l5():
    start = "1984"
    end = "2012"
    processed = proc.process_landsat_time_series(
        aoi=asset_id, start=start, end=end, dependent="NDVI", cloud=10
    )


def test_landsat_workflow_include_only_l8():
    start = "2013"
    end = "2018"
    processed = proc.process_landsat_time_series(
        aoi=asset_id, start=start, end=end, dependent="NDVI", cloud=10
    )


def test_landsat_workflow_include_both():
    start = "2000"
    end = "2018"
    processed = proc.process_landsat_time_series(
        aoi=asset_id, start=start, end=end, dependent="NDVI", cloud=10
    )
    processed.first().getInfo()
