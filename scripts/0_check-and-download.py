import os

from climateforcing.utils import check_and_download

here = os.path.dirname(os.path.realpath(__file__))

check_and_download(
    url='https://zenodo.org/record/4589756/files/rcmip-emissions-annual-means-v5-1-0.csv',
    filepath=os.path.join(here, '..', 'data_input', 'rcmip', 'rcmip-emissions-annual-means-v5-1-0.csv'),
)
check_and_download(
    url='https://zenodo.org/record/5513022/files/fair-1.6.2-wg3-params.json',
    filepath=os.path.join(here, '..', 'data_input', 'fair-1.6.2', 'fair-1.6.2-wg3-params.json'),
)
check_and_download(
    url='https://github.com/chrisroadmap/ar6/raw/main/data_output/tlm_lower_layer_warming_2015v1850-1900.csv',
    filepath=os.path.join(here, '..', 'data_input', 'wg1', 'temperature_ocean_2015.csv'),
)
