import os
import platform

import geemap


def vizualize_map(dataset, band, aoi):
    file_path = "map.html"
    Map = geemap.Map()
    Map.addLayerControl()
    Map.addLayer(dataset, {"bands": ["amp_1", "phase_1", "phase_2"]}, "True Colour")
    Map.centerObject(aoi, 10)
    Map.save(file_path)

    # Open the HTML file using the default web browser
    if platform.system() == "Windows":
        os.system(f"start {file_path}")
    elif platform.system() == "Darwin":  # macOS
        os.system(f"open {file_path}")
    else:  # Linux
        os.system(f"xdg-open {file_path}")
