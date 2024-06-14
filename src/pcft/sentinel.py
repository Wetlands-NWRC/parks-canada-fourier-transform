import ee


class Sentinel2SR(ee.ImageCollection):
    def __init__(self):
        super().__init__("COPERNICUS/S2_SR_HARMONIZED")

    def filterClouds(self, percent: float):
        return self.filter(ee.Filter.lte("CLOUDY_PIXEL_PERCENTAGE", percent))

    def applyCloudMask(self):
        return self.map(self.cloud_mask)

    @staticmethod
    def cloud_mask(image: ee.Image):
        qa = image.select("QA60")
        # Bits 10 and 11 are clouds and cirrus, respectively.
        cloud_bit_mask = 1 << 10
        cirrus_bit_mask = 1 << 11
        # Both flags should be set to zero, indicating clear conditions.
        mask = (
            qa.bitwiseAnd(cloud_bit_mask)
            .eq(0)
            .And(qa.bitwiseAnd(cirrus_bit_mask).eq(0))
        )

        return image.updateMask(mask)
