import json
import os

from climateforcing.utils import mkdir_p
import numpy as np
import pandas as pd
import scipy.linalg
from tqdm import tqdm

here = os.path.dirname(os.path.realpath(__file__))
mkdir_p(os.path.join(here, '..', 'data_output'))

with open(os.path.join(here, '..', 'data_input', 'fair-1.6.2', 'fair-1.6.2-wg3-params.json')) as f:
    config_list = json.load(f)

# required for running DICE
tstep = 5
n_box = 2
output=np.zeros((2237, 7))

for i in tqdm(range(2237)):
    # need edit to heat capacities (W m-2 K-1 yr)
    f2x = config_list[i]['F2x']
    ohc = [
        config_list[i]['ocean_heat_capacity'][0]/tstep,
        config_list[i]['ocean_heat_capacity'][1]/tstep
    ]
    oht = [
        config_list[i]['lambda_global'],
        config_list[i]['ocean_heat_exchange']
    ]
    eps = config_list[i]['deep_ocean_efficacy']

    eb_matrix = np.zeros((n_box, n_box))

    # First row
    eb_matrix[0, :2] = [
        -(oht[0]+eps*oht[1])/ohc[0],
        eps*oht[1]/ohc[0],
    ]

    # Last row
    eb_matrix[-1, -2:] = [
        oht[-1]/ohc[-1],
        -oht[-1]/ohc[-1]
    ]

    # Matrix exponential
    eb_matrix_d = scipy.linalg.expm(eb_matrix)
    eb_matrix_d

    forcing_vector = np.zeros(n_box)
    forcing_vector[0] = 1/ohc[0]
    forcing_vector_d = scipy.linalg.solve(eb_matrix, (eb_matrix_d - np.identity(n_box)) @ forcing_vector)
    forcing_vector_d

    solution5 = np.zeros((int(15000/tstep)+1, n_box))
#    for yr in range(1, len(solution5)):
#        solution5[yr, :] = eb_matrix_d @ solution5[yr-1, :] + forcing_vector_d * f2x
    output[i, 0:4] = eb_matrix_d.ravel()
    output[i, 4:6] = forcing_vector_d
    output[i, 6] = f2x

df = pd.DataFrame(output, columns=['a11','a12','a21','a22','b1','b2','f2x'])
df.to_csv(os.path.join(here, '..', 'data_output', 'climate_response_params.csv'))
