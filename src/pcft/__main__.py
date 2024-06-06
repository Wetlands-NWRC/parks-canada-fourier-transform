import sys

import ee

import geeft

from pcft.processing import process_s2, load_aoi
from pcft.visualize import vizualize_map
from pcft.plot import generate_plot


# Settings
AOI_FILENAME: str = 'users/ryangilberthamilton/ParksColab/PNP/pnp_aoi'
CLOUD = 1
START_DATE = '2018'
END_DATE = '2021'
DEPENDENT: str = 'NDVI'
MODES: int = 4


def main():
   
    description = f'pcft_{AOI_FILENAME.split("/")[-1].split(".")[0]}_{CLOUD}'
    aoi = load_aoi(AOI_FILENAME)
    
    s2_proc = process_s2(
       aoi=aoi,
       dependent=DEPENDENT,
       start=START_DATE,
       end=END_DATE,
       cloud=CLOUD
    )

    generate_plot(
        filename=f"{description}.png",
        dataset=s2_proc,
        cloud=CLOUD, 
        min_year=START_DATE,
        max_year=END_DATE
    )
    
    ft = geeft.compute(s2_proc, DEPENDENT, MODES)
    vizualize_map(ft.clip(aoi), None, aoi)
    # folder name = pcft_base_name of the aoi + cloud percent
    description = f'pcft_{AOI_FILENAME.split("/")[-1].split(".")[0]}_{CLOUD}'

    task = ee.batch.Export.image.toDrive(
        image=ft.clip(aoi),
        description=description,
        folder=description,
        fileNamePrefix=description,
        fileDimensions=[2048, 2048],
        scale=10,
        crs="EPSG:4326",
        region=aoi,
        skipEmptyTiles=True
    )

    start_task = input("start export task? [Y/n]")
    
    if start_task.lower() != 'n':
        sys.exit(1)
    
    task.start()
    print(f"Task: {task.id}")
    print(f"earthengine task info {task.id}")
    sys.exit(0)

if __name__ == '__main__':
    ee.Initialize()
    main()