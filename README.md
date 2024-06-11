# parks-canada-fourier-transform
project for exploratory analysis for fourier transform

# Setup
```bash
# create the base environment
conda create -n pcft -c conda-forge geemap geopandas matplotlib -y
```

```bash
# activate the environment
conda activate pcft
```

# IMPORTANT: THESE PACKAGES ARE NOT YET AVAILABLE ON PYPI OR CONDA FORGE

Install the Fouirer Transfrom lib from source
```bash
pip install git+https://github.com/Wetlands-NWRC/geeft.git
```

build from source
```bash
python git+https://github.com/Wetlands-NWRC/parks-canada-fourier-transform.git
```

# usage
```bash
# run the script, follow on screen instructions
(pcft) $ pcft
```

# install in dev mode
clone this repo

then run this command from the root of the repo
```bash
python -m pip install -e .
```

# update settings in __main__.py
lines 13 to 18 in __main__.py are where you would update the settings for the script
supports the following settings:
- `AOI_FILENAME` - both assets and shapefiles are supported
- `CLOUD` - cloud cover percentage
- `START_DATE` - start date for the time range (YYYY)
- `END_DATE` - end date for the time range + 1 (YYYY)
- `DEPENDENT` - the dependent variable to be used for the analysis
- `MODES` - the number of modes to be used for the analysis

notes:
- every time you change the settings, you do not need to re build the project, just run the script again with the new settings. This is because the project has been built in editable mode
- at this time the only support INDEX for the dependent variable is NDVI, but this can be expanded in the future
- You can also use any available bands in the original dataset as the dependent variable, plase note that they are the band names and not the band descriptions. See the Sentinel 2 product page on Google Earth Engine for more information on the bands available in the dataset.
