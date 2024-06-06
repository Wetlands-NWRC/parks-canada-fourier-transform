# parks-canada-fourier-transform
project for exploratory analysis for fourier transform

# Setup
```bash
# create the base environment
conda env create -f environment.yml
```

```bash
# activate the environment
conda activate pcft
```

# IMPORTANT: THESE PACKAGES ARE NOT YET AVAILABLE ON PYPI OR CONDA FORGE
# YOU WILL NEED TO INSTALL THEM MANUALLY FROM GITHUB REPOS
```bash
# install the remote sensing datasets library
pip install git+https://github.com/Wetlands-NWRC/geersd.git
```

```bash
# install fourer transform package
pip install git+https://github.com/Wetlands-NWRC/geeft.git
```