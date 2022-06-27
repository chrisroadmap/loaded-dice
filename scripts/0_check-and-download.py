from climateforcing.utils import check_and_download

check_and_download(
    url='https://zenodo.org/record/4589756/files/rcmip-emissions-annual-means-v5-1-0.csv',
    filepath='../data_input/rcmip/'
)
check_and_download(
    url='https://zenodo.org/record/5513022/files/fair-1.6.2-wg3-params.json',
    filepath='../data_input/fair-1.6.2/'
)
check_and_download(
    url='https://github.com/chrisroadmap/ar6/raw/main/data_output/tlm_lower_layer_warming_2015v1850-1900.csv',
    filepath='../data_input/wg1/'
)
