from typing import Callable

import math
import ee


def _get_names(prefix: str, frequences: list[int]) -> list[str]:
    return list(map(lambda x: f"{prefix}_{x}", frequences))


def _add_ndvi(nir: str, red: str) -> Callable:
    return lambda x: x.normalizedDifference([nir, red]).rename("NDVI").float()


def _add_constant(image: ee.Image) -> ee.Image:
    return image.addBands(ee.Image(1))


def _add_time(image: ee.Image) -> ee.Image:
    date = image.date()
    years = date.difference(ee.Date("1970-01-01"), "year")
    time_radians = ee.Image(years.multiply(2 * math.pi))
    return image.addBands(time_radians.rename("t").float())


def _add_harmonics(cos_names: list[str], sin_names: list[str]) -> Callable:
    freq = list(range(1, len(cos_names) + 1))

    def compute(image: ee.Image):
        frequencies = ee.Image.constant(freq)
        time = ee.Image(image).select("t")
        cosines = time.multiply(frequencies).cos().rename(cos_names)
        sines = time.multiply(frequencies).sin().rename(sin_names)
        return image.addBands(cosines).addBands(sines)

    return compute


def _compute_trend(
    dataset: ee.ImageCollection, dependent: str, independents: list[str]
):
    return dataset.select(independents + [dependent]).reduce(
        ee.Reducer.linearRegression(len(independents), 1)
    )


def _compute_coefficients(trend: ee.Image, indpendents: list[str]) -> ee.Image:
    return trend.select("coefficients").arrayFlatten([indpendents, ["coeff"]])


def _add_coef(coef: ee.Image) -> Callable:
    return lambda x: x.addBands(coef).select(".*coeff|NDVI")


def _add_phase(mode: int) -> Callable:
    sin, cos, name = f"sin_{mode}_coeff", f"cos_{mode}_coeff", f"phase_{mode}"
    return lambda x: x.addBands(
        x.select(sin).atan2(x.select(cos).unitScale(-math.pi, math.pi)).rename(name)
    )


def _add_amplitude(mode: int) -> Callable:
    sin, cos, name = f"sin_{mode}_coeff", f"cos_{mode}_coeff", f"amp_{mode}"
    return lambda x: x.addBands(x.select(sin).hypot(x.select(cos)).rename(name))


def compute(dataset: ee.ImageCollection, dependent: str, modes: int = 3):
    frequencies = list(range(1, modes + 1))
    cos_names = _get_names("cos", frequencies)
    sin_names = _get_names("sin", frequencies)

    independents = ["constant", "t"] + cos_names + sin_names

    dataset = (
        dataset.map(_add_constant)
        .map(_add_time)
        .map(_add_harmonics(cos_names=cos_names, sin_names=sin_names))
    )

    trend = _compute_trend(dataset, dependent, independents)
    coefficients = _compute_coefficients(trend, independents)

    dataset = dataset.map(_add_coef(coefficients))

    for mode in frequencies:
        dataset = dataset.map(_add_phase(mode)).map(_add_amplitude(mode))

    return dataset.median().unitScale(-1, 1)
