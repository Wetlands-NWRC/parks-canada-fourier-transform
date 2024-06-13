from typing import Any, Dict
import ee


class LandsatSR(ee.ImageCollection):
    def __init__(self, args: Any):
        super().__init__(args)

    def filterBounds(self, geometry: Dict[str, Any] | ee.Geometry) -> Any:
        return self.filter(ee.Filter.bounds(geometry))

    def filterDate(self, start, end):
        return self.filter(ee.Filter.date(start, end))

    def filterClouds(self, percent: float):
        return self.filter(ee.Filter.lte("CLOUD_COVER", percent))

    def applyCloudMask(self):
        return self.map(self.cloud_mask)

    def applyScalingFactor(self):
        return self.map(self.scaling_factors)

    @staticmethod
    def cloud_mask(image):
        """mask clouds and applies scaling factor"""
        qaMask = image.select("QA_PIXEL").bitwiseAnd(int("11111", 2)).eq(0)
        saturationMask = image.select("QA_RADSAT").eq(0)

        return image.updateMask(qaMask).updateMask(saturationMask)

    @staticmethod
    def scaling_factors(image: ee.Image):
        optical_bands = image.select("SR_B.").multiply(0.0000275).add(-0.2)
        thermal_bands = image.select("ST_B6").multiply(0.00341802).add(149.0)
        return image.addBands(optical_bands, None, True).addBands(
            thermal_bands, None, True
        )


class Landsat8SR(LandsatSR):
    def __init__(self):
        super().__init__("LANDSAT/LC08/C02/T1_L2")

    @staticmethod
    def scaling_factors(image: ee.Image):
        optical_bands = image.select("SR_B.").multiply(0.0000275).add(-0.2)
        thermal_bands = image.select("ST_B.*").multiply(0.00341802).add(149.0)
        return image.addBands(optical_bands, None, True).addBands(
            thermal_bands, None, True
        )


class Landsat7SR(LandsatSR):
    def __init__(self):
        super().__init__("LANDSAT/LE07/C02/T1_L2")

    def rename(self):
        """renames bands to match land sat 8"""
        old_names = ["SR_B1", "SR_B2", "SR_B3", "SR_B4", "SR_B5", "SR_B7"]
        new_name = ["SR_B2", "SR_B3", "SR_B4", "SR_B5", "SR_B6", "SR_B7"]
        return self.select(old_names, new_name)


class Landsat5SR(LandsatSR):
    def __init__(self):
        super().__init__("LANDSAT/LT05/C02/T1_L2")

    def rename(self):
        """renames bands to match land sat 8"""
        old_names = ["SR_B1", "SR_B2", "SR_B3", "SR_B4", "SR_B5", "SR_B7"]
        new_name = ["SR_B2", "SR_B3", "SR_B4", "SR_B5", "SR_B6", "SR_B7"]
        return self.select(old_names, new_name)
