import os

import matplotlib.pyplot as pl
import numpy as np
import pandas as pd

from fair.energy_balance_model import EnergyBalanceModel
from fair.forcing.ghg import meinshausen2020

here = os.path.dirname(os.path.realpath(__file__))

os.makedirs(os.path.join(here, '..', 'data_output', 'results'), exist_ok=True)

ensemble_size=1001

df_configs = pd.read_csv(os.path.join(here, '..', 'data_input', 'fair-2.1.0', 'calibrated_constrained_parameters.csv'), index_col=0)
configs = df_configs.index

pl.rcParams['figure.figsize'] = (12/2.54, 12/2.54)
pl.rcParams['font.size'] = 9
pl.rcParams['font.family'] = 'Arial'
pl.rcParams['ytick.direction'] = 'in'
pl.rcParams['ytick.minor.visible'] = True
pl.rcParams['ytick.major.right'] = True
pl.rcParams['ytick.right'] = True
pl.rcParams['xtick.direction'] = 'in'
pl.rcParams['xtick.minor.visible'] = True
pl.rcParams['xtick.major.top'] = True
pl.rcParams['xtick.top'] = True
pl.rcParams['axes.spines.top'] = True
pl.rcParams['axes.spines.bottom'] = True
pl.rcParams['figure.dpi'] = 150

for scenario in ['dice', 'dice_below2deg', 'dice_1p5deglowOS']:
    dfs = []
    outputs = {}
    outputs['CO2_concentration'] = np.ones((160, ensemble_size)) * np.nan
    outputs['temperature'] = np.ones((160, ensemble_size)) * np.nan
    outputs['social_cost_of_carbon'] = np.ones((160, ensemble_size)) * np.nan
    outputs['CO2_FFI_emissions'] = np.ones((160, ensemble_size)) * np.nan
    outputs['radiative_forcing'] = np.ones((160, ensemble_size)) * np.nan
    outputs['consumption_per_capita'] = np.ones((160, ensemble_size)) * np.nan
    outputs['interest_rate'] = np.ones((160, ensemble_size)) * np.nan

    # we still need the try-except because for some very strange reason 117814 failed silently in DICE
    for run, config in enumerate(configs[:ensemble_size]):
        try:
            df = pd.read_csv(os.path.join(here, "..", "data_output", scenario, f"{config:07d}.csv"), index_col=0)
            outputs['CO2_concentration'][:, run] = df.loc['Atmospheric concentrations ppm']
            outputs['temperature'][:, run] = df.loc['Atmospheric Temperature rel. 1850-1900']
            outputs['social_cost_of_carbon'][:, run] = df.loc['Social cost of carbon']
            outputs['CO2_FFI_emissions'][:, run] = df.loc['Industrial Emissions GTCO2 per year']
            outputs['radiative_forcing'][:, run] = df.loc['Forcings']
            outputs['consumption_per_capita'][:, run] = df.loc['Consumption Per Capita ']
            outputs['interest_rate'][:, run] = df.loc['Interest Rate ']
        except:
            pass

    print('emissions   2101', np.nanpercentile(outputs['CO2_FFI_emissions'][27, :], (5, 50, 95)))  # CO2 fossil emissions 2100
    print('SCC         2023', np.nanpercentile(outputs['social_cost_of_carbon'][0, :], (5, 50, 95))) # social cost of carbon 2020
    print('temperature 2101', np.nanpercentile(outputs['temperature'][27, :], (5, 50, 95)))  # temperature 2100
    print('temperature peak', np.nanpercentile(np.max(outputs['temperature'], axis=0), (5, 50, 95)))  # peak temperature
    print('forcing     2101', np.nanpercentile(outputs['radiative_forcing'][27, :], (5, 50, 95)))  # radiative forcing 2100

    for variable in ['CO2_concentration', 'temperature', 'social_cost_of_carbon', 'CO2_FFI_emissions', 'radiative_forcing', 'consumption_per_capita', 'interest_rate']:
        df = pd.DataFrame(outputs[variable].T, columns = np.arange(2023, 2503, 3), index = configs)
        df.to_csv(os.path.join(here, '..', 'data_output', 'results', f'{scenario}__{variable}.csv'))
