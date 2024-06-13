import ee


ee.Initialize()


test_point_aoi = ee.geometry.Geometry.Point([-77.2587941022832, 44.031755844102214])
expected_l5_l7_bands = ["SR_B2", "SR_B3", "SR_B4", "SR_B5", "SR_B6", "SR_B7"]


def get_image_props(image) -> list[str]:
    return image.propertyNames().getInfo()
