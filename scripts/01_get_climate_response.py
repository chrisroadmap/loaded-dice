import os

import numpy as np
import pandas as pd
from tqdm import tqdm
import scipy.linalg

from fair.energy_balance_model import EnergyBalanceModel

# We run FaIR projections on a three year timestep twice; first to 2500 to get
# the non-CO2 forcing including uncertainty, and second to 2020 to get the
# C-cycle spin-ups.

here = os.path.dirname(os.path.realpath(__file__))
os.makedirs(os.path.join(here, '..', 'data_output', 'climate_configs'), exist_ok=True)

calibration = pd.read_csv(os.path.join(here, '..', 'data_input', 'fair-2.1.0', 'ar6_calibration_ebm3.csv'), index_col=0)
configs = calibration.index

# required for running DICE
tstep = 3
n_box = 3
output=np.zeros((1001, 12))

for i, config in tqdm(enumerate(configs)):
    ebm = EnergyBalanceModel(
        ocean_heat_capacity = calibration.loc[config, 'c1':'c3'],
        ocean_heat_transfer = calibration.loc[config, 'kappa1':'kappa3'],
        deep_ocean_efficacy = calibration.loc[config, 'epsilon'],
        gamma_autocorrelation = calibration.loc[config, 'gamma'],
        timestep=tstep,
        stochastic_run=False,
    )
    A = ebm.eb_matrix_d
    B = ebm.forcing_vector_d

    output[i, 0:9] = A[1:, 1:].ravel()
    output[i, 9:12] = A[1:, 0] + B[1:]

df = pd.DataFrame(output, columns=['a11','a12','a13','a21','a22','a23','a31','a32','a33','b1','b2','b3'], index=configs)
df.to_csv(os.path.join(here, '..', 'data_output', 'climate_configs', 'climate_response_params.csv'))
