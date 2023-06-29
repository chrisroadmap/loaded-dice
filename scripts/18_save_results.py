import os

import numpy as np
import pandas as pd

from fair.energy_balance_model import EnergyBalanceModel
from fair.forcing.ghg import meinshausen2020

here = os.path.dirname(os.path.realpath(__file__))

os.makedirs(os.path.join(here, '..', 'data_output', 'results'), exist_ok=True)

ensemble_size=1001
year = np.arange(2023, 2503, 3)

df_configs = pd.read_csv(os.path.join(here, '..', 'data_input', 'fair-2.1.0', 'calibrated_constrained_parameters.csv'), index_col=0)
configs = df_configs.index

for scenario in ['dice', 'dice_below2deg', 'dice_1p5deglowOS']:
    dfs = []
    outputs = {}
    outputs['CO2_concentration'] = np.ones((160, ensemble_size)) * np.nan
    outputs['temperature'] = np.ones((160, ensemble_size)) * np.nan
    outputs['social_cost_of_carbon'] = np.ones((160, ensemble_size)) * np.nan
    outputs['CO2_FFI_emissions'] = np.ones((160, ensemble_size)) * np.nan
    outputs['CO2_AFOLU_emissions'] = np.ones((160, ensemble_size)) * np.nan
    outputs['CO2_total_emissions'] = np.ones((160, ensemble_size)) * np.nan
    outputs['radiative_forcing'] = np.ones((160, ensemble_size)) * np.nan
    outputs['consumption_per_capita'] = np.ones((160, ensemble_size)) * np.nan
    outputs['interest_rate'] = np.ones((160, ensemble_size)) * np.nan
    outputs['net_zero_year'] = np.ones(ensemble_size) * np.nan

    for run, config in enumerate(configs[:ensemble_size]):
        df = pd.read_csv(os.path.join(here, "..", "data_output", scenario, f"{config:07d}.csv"), index_col=0)
        outputs['CO2_concentration'][:, run] = df.loc['Atmospheric concentrations ppm']
        outputs['temperature'][:, run] = df.loc['Atmospheric Temperature rel. 1850-1900']
        outputs['social_cost_of_carbon'][:, run] = df.loc['Social cost of carbon']
        outputs['CO2_FFI_emissions'][:, run] = df.loc['Industrial Emissions GTCO2 per year']
        outputs['CO2_AFOLU_emissions'][:, run] = df.loc['Land emissions']
        outputs['CO2_total_emissions'][:, run] = df.loc['Industrial Emissions GTCO2 per year'] + df.loc['Land emissions']
        outputs['radiative_forcing'][:, run] = df.loc['Forcings']
        outputs['consumption_per_capita'][:, run] = df.loc['Consumption Per Capita ']
        outputs['interest_rate'][:, run] = df.loc['Interest Rate ']

        # calculate net zero year
        co2 = outputs['CO2_total_emissions'][:, run]
        zc1 = np.where(np.diff(np.sign(co2)))[0][0]  # index before
        zc2 = zc1 + 1
        frac = co2[zc2]/(co2[zc2]-co2[zc1])
        outputs['net_zero_year'][run] = year[zc1] * frac + year[zc2] * (1-frac)

    for variable in ['CO2_concentration', 'temperature', 'social_cost_of_carbon', 'CO2_FFI_emissions', 'CO2_AFOLU_emissions', 'CO2_total_emissions', 'radiative_forcing', 'consumption_per_capita', 'interest_rate']:
        df = pd.DataFrame(outputs[variable].T, columns = np.arange(2023, 2503, 3), index = configs)
        df.to_csv(os.path.join(here, '..', 'data_output', 'results', f'{scenario}__{variable}.csv'))
    df = pd.DataFrame(outputs['net_zero_year'], index = configs)
    df.to_csv(os.path.join(here, '..', 'data_output', 'results', f'{scenario}__net_zero_year.csv'))
