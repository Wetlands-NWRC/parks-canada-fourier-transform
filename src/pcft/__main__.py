import sys

import ee

import geeft

from pcft.user_input import get_user_input
from pcft.processing import process_l8, load_aoi
from pcft.visualize import vizualize_map
from pcft.plot import generate_plot


def main():

    user_input = get_user_input()
    description = f'pcft_{user_input.aoi_file_name.split("/")[-1].split(".")[0]}_{user_input.cloud_percent}'
    aoi = load_aoi(user_input.aoi_file_name)

    l8_proc = process_l8(
        aoi=aoi,
        dependent=user_input.dependent,
        start=user_input.start_date,
        end=user_input.end_date,
        cloud=user_input.cloud_percent,
    )

    generate_plot(
        filename=f"{description}.png",
        dataset=l8_proc,
        cloud=user_input.cloud_percent,
        min_year=user_input.start_date,
        max_year=user_input.end_date,
    )

    ft = geeft.compute(l8_proc, user_input.dependent, user_input.modes)
    vizualize_map(ft.clip(aoi), None, aoi)
    # folder name = pcft_base_name of the aoi + cloud percent

    task = ee.batch.Export.image.toDrive(
        image=ft.clip(aoi),
        description=description,
        folder=description,
        fileNamePrefix=description,
        fileDimensions=[2048, 2048],
        scale=10,
        crs="EPSG:4326",
        region=aoi,
        skipEmptyTiles=True,
    )

    start_task = input("start export task? [Y/n]: ")

    if start_task.lower().strip() == "n":
        sys.exit(1)

    task.start()
    print(f"Task: {task.id}")
    print(f"earthengine task info {task.id}")
    sys.exit(0)


if __name__ == "__main__":
    ee.Initialize()
    main()
