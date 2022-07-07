import os

from climateforcing.utils import mkdir_p
import matplotlib.pyplot as pl
import numpy as np
import pandas as pd

here = os.path.dirname(os.path.realpath(__file__))

mkdir_p(os.path.join(here, '..', 'figures'))

ensemble_size=2237

outputs = {}
outputs['CO2'] = np.ones((100, ensemble_size))
outputs['T'] = np.ones((100, ensemble_size))
outputs['carbon_price'] = np.ones((100, ensemble_size))
outputs['SCC'] = np.ones((100, ensemble_size))
outputs['E'] = np.ones((100, ensemble_size))
outputs['F'] = np.ones((100, ensemble_size))

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

dfs = []
for run in range(ensemble_size):
    dfs.append(pd.read_csv(os.path.join(here, "..", "data_output", "dice", f"{run:04d}.csv"), index_col=0))

for run in range(ensemble_size):
    outputs['CO2'][:, run] = dfs[run].loc['Atmospheric concentrations ppm']
    outputs['T'][:, run] = dfs[run].loc['Atmospheric Temperature rel. 1850-1900']
    outputs['carbon_price'][:, run] = dfs[run].loc['Carbon Price (per t CO2)']
    outputs['SCC'][:, run] = dfs[run].loc['Social cost of carbon']
    outputs['E'][:, run] = dfs[run].loc['Industrial Emissions GTCO2 per year']
    outputs['F'][:, run] = dfs[run].loc['Forcings']

print(np.percentile(outputs['E'][17, :], (5, 50, 95)))  # CO2 fossil emissions 2100
print(np.percentile(outputs['SCC'][1, :], (5, 50, 95))) # social cost of carbon 2020
print(np.percentile(outputs['T'][17, :], (5, 50, 95)))  # temperature 2100
print(np.percentile(outputs['F'][17, :], (5, 50, 95)))  # radiative forcing 2100

fig, ax = pl.subplots(2,2)

yunit = {
    'E': 'GtCO$_2$ yr$^{-1}$',
    'CO2': 'ppm',
    'T': '°C relative to 1850-1900',
    'SCC': '\$(2005) tCO$_2^{-1}$'
}
title = {
    'E': 'CO$_2$ fossil emissions',
    'CO2': 'CO$_2$ concentrations',
    'T': 'Global mean surface temperature',
    'SCC': 'Social cost of carbon'
}
ylim = {
    'E': (-10, 60),
    'CO2': (400, 750),
    'T': (0.5, 4),
    'SCC': (0, 500)
}


for i, var in enumerate(['E', 'CO2', 'T', 'SCC']):
    ax[i//2,i%2].fill_between(
        np.arange(2015, 2515, 5),
        np.percentile(outputs[var], 5, axis=1),
        np.percentile(outputs[var], 95, axis=1),
        color='0.8'
    )
    ax[i//2,i%2].fill_between(
        np.arange(2015, 2515, 5),
        np.percentile(outputs[var], 16, axis=1),
        np.percentile(outputs[var], 84, axis=1),
        color='0.6'
    )
    ax[i//2,i%2].plot(np.arange(2015, 2515, 5), np.median(outputs[var], axis=1), color='k')
    ax[i//2,i%2].set_xlim(2020,2125)
    ax[i//2,i%2].set_title(title[var])
    ax[i//2,i%2].set_ylabel(yunit[var])
    ax[i//2,i%2].set_ylim(ylim[var])
    ax[i//2,i%2].set_xticks(np.arange(2025, 2130, 25))
    ax[i//2,i%2].axhline(0, ls=':', color='k')
fig.tight_layout()
pl.savefig(os.path.join(here, '..', 'figures', 'climate_projections.png'))
pl.savefig(os.path.join(here, '..', 'figures', 'climate_projections.pdf'))
pl.show()


#pl.hist(scc2020)
#pl.show()
