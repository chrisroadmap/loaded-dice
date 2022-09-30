import os

import matplotlib.pyplot as pl
import numpy as np
import pandas as pd

here = os.path.dirname(os.path.realpath(__file__))

os.makedirs(os.path.join(here, '..', 'figures'), exist_ok=True)

ensemble_size=1001

df_configs = pd.read_csv(os.path.join(here, '..', 'data_input', 'fair-2.1.0', 'ar6_calibration_ebm3.csv'), index_col=0)
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

for scenario in ['dice_1p5deglowOS']:
    dfs = []
    outputs = {}
    outputs['CO2'] = np.ones((100, ensemble_size)) * np.nan
    outputs['T'] = np.ones((100, ensemble_size)) * np.nan
    outputs['carbon_price'] = np.ones((100, ensemble_size)) * np.nan
    outputs['SCC'] = np.ones((100, ensemble_size)) * np.nan
    outputs['E'] = np.ones((100, ensemble_size)) * np.nan
    outputs['F'] = np.ones((100, ensemble_size)) * np.nan
    for run, config in enumerate(configs[:ensemble_size]):
        try:
            dfs.append(pd.read_csv(os.path.join(here, "..", "data_output", scenario, f"{config:07d}.csv"), index_col=0))
        except:
            pass

    for run in range(ensemble_size):
        try:
            outputs['CO2'][:, run] = dfs[run].loc['Atmospheric concentrations ppm']
            outputs['T'][:, run] = dfs[run].loc['Atmospheric Temperature rel. 1850-1900']
            outputs['carbon_price'][:, run] = dfs[run].loc['Carbon Price (per t CO2)']
            outputs['SCC'][:, run] = dfs[run].loc['Social cost of carbon']
            outputs['E'][:, run] = dfs[run].loc['Industrial Emissions GTCO2 per year']
            outputs['F'][:, run] = dfs[run].loc['Forcings']
        except:
            pass

    print('emissions   2100', np.nanpercentile(outputs['E'][16, :], (5, 50, 95)))  # CO2 fossil emissions 2100
    print('SCC         2020', np.nanpercentile(outputs['SCC'][0, :], (5, 50, 95))) # social cost of carbon 2020
    print('temperature 2100', np.nanpercentile(outputs['T'][16, :], (5, 50, 95)))  # temperature 2100
    print('temperature peak', np.nanpercentile(np.max(outputs['T'], axis=0), (5, 50, 95)))  # peak temperature
    print('forcing     2100', np.nanpercentile(outputs['F'][16, :], (5, 50, 95)))  # radiative forcing 2100

    fig, ax = pl.subplots(2,2)

    yunit = {
        'E': 'GtCO$_2$ yr$^{-1}$',
        'CO2': 'ppm',
        'T': '°C relative to 1850-1900',
        'SCC': '\$(2020) tCO$_2^{-1}$'
    }
    title = {
        'E': 'CO$_2$ fossil emissions',
        'CO2': 'CO$_2$ concentrations',
        'T': 'Global mean surface temperature',
        'SCC': 'Social cost of carbon'
    }
    ylim = {
        'E': (-10, 60),
        'CO2': (350, 750),
        'T': (0.5, 4),
        'SCC': (0, 1000)
    }


    for i, var in enumerate(['E', 'CO2', 'T', 'SCC']):
        ax[i//2,i%2].fill_between(
            np.arange(2020, 2520, 5),
            np.nanpercentile(outputs[var], 5, axis=1),
            np.nanpercentile(outputs[var], 95, axis=1),
            color='0.8'
        )
        ax[i//2,i%2].fill_between(
            np.arange(2020, 2520, 5),
            np.nanpercentile(outputs[var], 16, axis=1),
            np.nanpercentile(outputs[var], 84, axis=1),
            color='0.6'
        )
        ax[i//2,i%2].plot(np.arange(2020, 2520, 5), np.nanmedian(outputs[var], axis=1), color='k')
        ax[i//2,i%2].set_xlim(2020,2125)
        ax[i//2,i%2].set_title(title[var])
        ax[i//2,i%2].set_ylabel(yunit[var])
        ax[i//2,i%2].set_ylim(ylim[var])
        ax[i//2,i%2].set_xticks(np.arange(2025, 2130, 25))
        ax[i//2,i%2].axhline(0, ls=':', color='k')
    fig.tight_layout()
    pl.savefig(os.path.join(here, '..', 'figures', f'climate_projections_{scenario}.png'))
    pl.savefig(os.path.join(here, '..', 'figures', f'climate_projections_{scenario}.pdf'))
    pl.show()
