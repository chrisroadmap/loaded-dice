import os

import matplotlib.pyplot as pl
from matplotlib.ticker import ScalarFormatter
import numpy as np
import pandas as pd

from fair.energy_balance_model import EnergyBalanceModel
from fair.forcing.ghg import meinshausen2020

here = os.path.dirname(os.path.realpath(__file__))

os.makedirs(os.path.join(here, '..', 'figures'), exist_ok=True)

ensemble_size=1001

df_configs = pd.read_csv(os.path.join(here, '..', 'data_input', 'fair-2.1.0', 'ar6_calibration_ebm3.csv'), index_col=0)
configs = df_configs.index

ecs = np.zeros(1001)
tcr = np.zeros(1001)

erf_2co2 = meinshausen2020(
    np.array([554.30, 731.41, 273.87]) * np.ones((1, 1, 1, 3)),
    np.array([277.15, 731.41, 273.87]) * np.ones((1, 1, 1, 3)),
    np.array((1.05, 0.86, 1.07)) * np.ones((1, 1, 1, 1)),
    np.ones((1, 1, 1, 3)),
    np.array([True, False, False]),
    np.array([False, True, False]),
    np.array([False, False, True]),
    np.array([False, False, False])
).squeeze()[0]
calibrated_f4co2_mean = df_configs['F_4xCO2'].mean()

for i, config in enumerate(configs):
    ebm = EnergyBalanceModel(
        ocean_heat_capacity = df_configs.loc[config, 'c1':'c3'],
        ocean_heat_transfer = df_configs.loc[config, 'kappa1':'kappa3'],
        deep_ocean_efficacy = df_configs.loc[config, 'epsilon'],
        gamma_autocorrelation = df_configs.loc[config, 'gamma'],
        forcing_4co2 = 2 * erf_2co2 * (1 + 0.561*(calibrated_f4co2_mean - df_configs.loc[config, 'F_4xCO2'])/calibrated_f4co2_mean),
        timestep=5,
        stochastic_run=False,
    )
    ebm.emergent_parameters()
    ecs[i], tcr[i] = (ebm.ecs, ebm.tcr)

pl.rcParams['figure.figsize'] = (40.1/2.54, 30/2.54)
pl.rcParams['font.size'] = 16 #20
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
    'CO2_FFI_emissions': '(a) CO$_2$ fossil emissions',
    'CO2_concentration': '(b) CO$_2$ concentrations',
    'temperature': '(d) Surface temperature',
    'social_cost_of_carbon': 'Social cost of carbon',
    'radiative_forcing': '(e) Effective radiative forcing'
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
    print('emissions   2050', np.nanpercentile(outputs[scenario]['CO2_FFI_emissions'][10, :], (5, 50, 95)))  # CO2 fossil emissions 2100
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

fig, ax = pl.subplots(2,3)
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
ax[1,0].legend(fontsize=14, frameon=False)
fig.tight_layout()
#pl.savefig(os.path.join(here, '..', 'figures', f'climate_projections.png'))
#pl.savefig(os.path.join(here, '..', 'figures', f'climate_projections.pdf'))
#pl.show()

#pl.rcParams['figure.figsize'] = (20/2.54, 20/2.54)
#fig, ax = pl.subplots(1, 1)
for scenario in ['dice', 'dice_below2deg', 'dice_1p5deglowOS']:
    ax[0,2].hist(
        outputs[scenario]['social_cost_of_carbon'][0, :],
        alpha=0.5,
        label=labels[scenario],
        color=colors[scenario],
        density=True,
        bins=np.logspace(-1, 4, 101),
        log=True
    )
ax[0,2].set_xscale('log')
pl.rcParams['xtick.minor.visible'] = True
ax[0,2].set_xlim(6, 10000)
ax[0,2].set_title("(c) Social cost of carbon in 2023")
ax[0,2].set_xlabel("(2020\$)")
ax[0,2].set_ylabel("Density")
ax[0,2].set_yticklabels([])
ax[0,2].xaxis.set_major_formatter(ScalarFormatter())


for scenario in ['dice', 'dice_below2deg', 'dice_1p5deglowOS']:
    ax[1,2].scatter(ecs, outputs[scenario]['social_cost_of_carbon'][0, :], alpha=0.3, label=labels[scenario], color=colors[scenario])
ax[1,2].set_yscale('log')
ax[1,2].set_xlim(1, 7)
ax[1,2].set_ylim(5, 10000)
ax[1,2].set_title("(f) Equilibrium climate sensitivity")
ax[1,2].set_ylabel("Social cost of carbon, 2020\$")
ax[1,2].set_xlabel("ECS, °C")
ax[1,2].yaxis.set_major_formatter(ScalarFormatter())

#ax.yaxis.set_major_formatter(ScalarFormatter())
#ax.legend(fontsize=14, frameon=False)
fig.tight_layout()
#pl.savefig(os.path.join(here, '..', 'figures', f'scc_histogram.png'))
#pl.savefig(os.path.join(here, '..', 'figures', f'scc_histogram.pdf'))
pl.savefig(os.path.join(here, '..', 'figures', f'iamc_all.png'))
pl.savefig(os.path.join(here, '..', 'figures', f'iamc_all.pdf'))
pl.show()
