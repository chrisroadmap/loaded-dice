import os

import numpy as np
import pandas as pd
from tqdm import tqdm
import scipy.linalg

from fair.energy_balance_model import EnergyBalanceModel

# We run FaIR projections on a five year timestep twice; first to 2500 to get
# the non-CO2 forcing including uncertainty, and second to 2020 to get the
# C-cycle spin-ups.

here = os.path.dirname(os.path.realpath(__file__))
os.makedirs(os.path.join(here, '..', 'data_output', 'climate_configs'), exist_ok=True)

calibration = pd.read_csv(os.path.join(here, '..', 'data_input', 'fair-2.1.0', 'ar6_calibration_ebm3.csv'), index_col=0)
configs = calibration.index

# required for running DICE
tstep = 5
n_box = 3
output=np.zeros((1001, 12))

for i, config in tqdm(enumerate(configs)):
    ebm = EnergyBalanceModel(
        ocean_heat_capacity = calibration.loc[config, 'c1':'c3'],
        ocean_heat_transfer = calibration.loc[config, 'kappa1':'kappa3'],
        deep_ocean_efficacy = calibration.loc[config, 'epsilon'],
        gamma_autocorrelation = calibration.loc[config, 'gamma'],
        timestep=5,
        stochastic_run=False,
    )
    A = ebm.eb_matrix_d
    B = ebm.forcing_vector_d

    #forcing_vector = A[1:, 0] + B[1:]
    output[i, 0:9] = A[1:, 1:].ravel()
    output[i, 9:12] = A[1:, 0] + B[1:]
    # # need edit to heat capacities (W m-2 K-1 yr)
    # ohc = [
    #     calibration.loc[config, 'c1']/tstep,
    #     calibration.loc[config, 'c2']/tstep,
    #     calibration.loc[config, 'c3']/tstep
    # ]
    # oht = [
    #     calibration.loc[config, 'kappa1'],
    #     calibration.loc[config, 'kappa2'],
    #     calibration.loc[config, 'kappa3']
    # ]
    # eps = calibration.loc[config, 'epsilon']
    #
    # eb_matrix = np.zeros((n_box, n_box))
    #
    # # First row
    # eb_matrix[0, :2] = [
    #     -(oht[0]+eps*oht[1])/ohc[0],
    #     eps*oht[1]/ohc[0],
    # ]
    #
    # # Last row
    # eb_matrix[-1, -2:] = [
    #     oht[-1]/ohc[-1],
    #     -oht[-1]/ohc[-1]
    # ]
    #
    # # intermediate rows
    # row = 1
    # eb_matrix[row, row - 1 : row + 2] = [
    #     oht[row] / ohc[row],
    #     -(oht[row] + eps * oht[row + 1])/ ohc[row],
    #     eps * oht[row + 1] / ohc[row],
    # ]
    #
    # # Matrix exponential
    # eb_matrix_d = scipy.linalg.expm(eb_matrix)
    # eb_matrix_d
    #
    # forcing_vector = np.zeros(n_box)
    # forcing_vector[0] = 1/ohc[0]
    # forcing_vector_d = scipy.linalg.solve(eb_matrix, (eb_matrix_d - np.identity(n_box)) @ forcing_vector)
    # forcing_vector_d
    # output[i, 0:9] = eb_matrix_d.ravel()
    # output[i, 9:12] = forcing_vector_d

df = pd.DataFrame(output, columns=['a11','a12','a13','a21','a22','a23','a31','a32','a33','b1','b2','b3'], index=configs)
df.to_csv(os.path.join(here, '..', 'data_output', 'climate_configs', 'climate_response_params.csv'))
