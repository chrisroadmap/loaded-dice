import os

import matplotlib.pyplot as pl
import numpy as np
import pandas as pd

from fair.energy_balance_model import EnergyBalanceModel
from fair.forcing.ghg import meinshausen2020

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

yunit = {
    'CO2_FFI_emissions': 'GtCO$_2$ yr$^{-1}$',
    'CO2_concentration': 'ppm',
    'temperature': '°C relative to 1850-1900',
    'social_cost_of_carbon': '\$(2020) tCO$_2^{-1}$',
    'radiative_forcing': 'W m$^{-2}$'
}
title = {
    'CO2_FFI_emissions': 'CO$_2$ fossil emissions',
    'CO2_concentration': 'CO$_2$ concentrations',
    'temperature': 'Global mean surface temperature',
    'social_cost_of_carbon': 'Social cost of carbon',
    'radiative_forcing': 'Effective radiative forcing'
}
ylim = {
    'CO2_FFI_emissions': (-20, 55),
    'CO2_concentration': (300, 750),
    'temperature': (0.5, 4),
    'social_cost_of_carbon': (0, 4000),
    'radiative_forcing': (0, 7)
}
labels = {
    'dice': "'Nordhaus optimal'",
    'dice_below2deg': "Well-below 2°C",
    'dice_1p5deglowOS': "1.5°C-low overshoot"
}
colors = {
    'dice': "#003f5c",
    'dice_below2deg': "#bc5090",
    'dice_1p5deglowOS': "#ffa600"
}

outputs = {}

for scenario in ['dice', 'dice_below2deg', 'dice_1p5deglowOS']:
    outputs[scenario] = {}
    for variable in ['CO2_concentration', 'temperature', 'social_cost_of_carbon', 'CO2_FFI_emissions', 'radiative_forcing']:
        df = pd.read_csv(os.path.join(here, '..', 'data_output', 'results', f'{scenario}__{variable}.csv'), index_col=0)
        outputs[scenario][variable] = df[:].T.values

    print('emissions   2101', np.nanpercentile(outputs[scenario]['CO2_FFI_emissions'][27, :], (5, 50, 95)))  # CO2 fossil emissions 2100
    print('SCC         2023', np.nanpercentile(outputs[scenario]['social_cost_of_carbon'][0, :], (5, 50, 95))) # social cost of carbon 2020
    print('temperature 2101', np.nanpercentile(outputs[scenario]['temperature'][27, :], (5, 50, 95)))  # temperature 2100
    print('temperature peak', np.nanpercentile(np.max(outputs[scenario]['temperature'], axis=0), (5, 50, 95)))  # peak temperature
    print('forcing     2101', np.nanpercentile(outputs[scenario]['radiative_forcing'][27, :], (5, 50, 95)))  # radiative forcing 2100

    # fig, ax = pl.subplots(2,2)
    # for i, variable in enumerate(['CO2_FFI_emissions', 'CO2_concentration', 'temperature', 'social_cost_of_carbon']):
    #     ax[i//2,i%2].fill_between(
    #         np.arange(2023, 2134, 3),
    #         np.nanpercentile(outputs[scenario][variable][:37, :], 5, axis=1),
    #         np.nanpercentile(outputs[scenario][variable][:37, :], 95, axis=1),
    #         color=colors[scenario],
    #         alpha=0.2
    #     )
    #     ax[i//2,i%2].fill_between(
    #         np.arange(2023, 2134, 3),
    #         np.nanpercentile(outputs[scenario][variable][:37, :], 16, axis=1),
    #         np.nanpercentile(outputs[scenario][variable][:37, :], 84, axis=1),
    #         color=colors[scenario],
    #         alpha=0.2
    #     )
    #     ax[i//2,i%2].plot(
    #         np.arange(2023, 2134, 3),
    #         np.nanmedian(outputs[scenario][variable][:37, :], axis=1),
    #         color=colors[scenario]
    #     )
    #     ax[i//2,i%2].set_xlim(2023,2125)
    #     ax[i//2,i%2].set_title(title[variable])
    #     ax[i//2,i%2].set_ylabel(yunit[variable])
    #     ax[i//2,i%2].set_ylim(ylim[variable])
    #     ax[i//2,i%2].set_xticks(np.arange(2025, 2130, 25))
    #     ax[i//2,i%2].axhline(0, ls=':', color='k')
    # fig.tight_layout()
    # pl.savefig(os.path.join(here, '..', 'figures', f'climate_projections_{scenario}.png'))
    # pl.savefig(os.path.join(here, '..', 'figures', f'climate_projections_{scenario}.pdf'))
    # pl.show()

fig, ax = pl.subplots(2,2)
for i, variable in enumerate(['CO2_FFI_emissions', 'CO2_concentration', 'temperature', 'radiative_forcing']):
    for scenario in ['dice', 'dice_below2deg', 'dice_1p5deglowOS']:
        ax[i//2,i%2].fill_between(
            np.arange(2023, 2134, 3),
            np.nanpercentile(outputs[scenario][variable][:37, :], 5, axis=1),
            np.nanpercentile(outputs[scenario][variable][:37, :], 95, axis=1),
            color=colors[scenario],
            alpha=0.2,
            lw=0
        )
        ax[i//2,i%2].fill_between(
            np.arange(2023, 2134, 3),
            np.nanpercentile(outputs[scenario][variable][:37, :], 16, axis=1),
            np.nanpercentile(outputs[scenario][variable][:37, :], 84, axis=1),
            color=colors[scenario],
            alpha=0.2,
            lw=0
        )
        ax[i//2,i%2].plot(
            np.arange(2023, 2134, 3),
            np.nanmedian(outputs[scenario][variable][:37, :], axis=1),
            color=colors[scenario],
            label=labels[scenario],
        )
    ax[i//2,i%2].set_xlim(2023,2125)
    ax[i//2,i%2].set_title(title[variable])
    ax[i//2,i%2].set_ylabel(yunit[variable])
    ax[i//2,i%2].set_ylim(ylim[variable])
    ax[i//2,i%2].set_xticks(np.arange(2025, 2130, 25))
    ax[i//2,i%2].axhline(0, ls=':', color='k')
    ax[i//2,i%2].axvline(2100, ls=':', color='k')
ax[1,0].legend(fontsize=6, frameon=False)
fig.tight_layout()
pl.savefig(os.path.join(here, '..', 'figures', f'climate_projections.png'))
pl.savefig(os.path.join(here, '..', 'figures', f'climate_projections.pdf'))
pl.show()


fig, ax = pl.subplots(1, 1)
for scenario in ['dice', 'dice_below2deg', 'dice_1p5deglowOS']:
    ax.hist(
        outputs[scenario]['social_cost_of_carbon'][0, :],
        alpha=0.3,
        label=labels[scenario],
        color=colors[scenario],
        density=True,
        bins=np.logspace(-1, 4, 51),
        log=True
    )
    pl.xscale('log')
ax.set_xlim(6, 10000)
ax.set_title("Social cost of carbon in 2023")
ax.set_xlabel("(2020\$)")
ax.legend()
fig.tight_layout()
pl.savefig(os.path.join(here, '..', 'figures', f'scc_histogram.png'))
pl.savefig(os.path.join(here, '..', 'figures', f'scc_histogram.pdf'))
pl.show()
