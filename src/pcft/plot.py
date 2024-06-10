import ee

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt


def date_time_scatter_plot(
    df: gpd.GeoDataFrame | pd.DataFrame, cloud, min_year, max_year
):
    # Create a scatter plot
    fig, ax = plt.subplots()
    # Create a scatter plot on the axes

    ax.scatter(df["doy"], df["year"], alpha=0.5)

    # Set the limits for the x-axis and y-axis
    ax.set_xlim([1, 366])  # Julian dates range from 1 to 366
    ax.set_ylim(
        [df["year"].min() - 1, df["year"].max() + 1]
    )  # Years range from min to max year in the data

    # Set major tick marks every 50 on the x-axis and every 1 on the y-axis
    ax.set_xticks(range(0, 366, 50))
    ax.set_yticks(range(int(min_year) - 1, int(max_year) + 1, 1))

    ax.set_xlabel("DOY")
    ax.set_ylabel("Year")
    ax.set_title(f"Valid Observations: CLOUD = {cloud}")

    ax.grid(True)
    return fig


def _convert_ic_to_fc(dataset) -> pd.DataFrame:
    def _image2feature(element: ee.Image):
        x = ee.Image(element)
        return ee.Feature(x.geometry(), x.toDictionary(x.propertyNames()))

    element_list = dataset.toList(dataset.size())
    elem2feat = element_list.map(_image2feature)
    fc = ee.FeatureCollection(elem2feat)

    gdf = gpd.GeoDataFrame.from_features(fc.getInfo()["features"])
    return gdf[["year", "doy"]].astype(int)


def generate_plot(filename: str, dataset, cloud, min_year, max_year) -> None:
    as_table = _convert_ic_to_fc(dataset)
    plot = date_time_scatter_plot(
        as_table, cloud=cloud, min_year=min_year, max_year=max_year
    )
    plot.savefig(filename)
    return None
