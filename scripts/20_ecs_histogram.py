import os

import matplotlib.pyplot as pl
from matplotlib.ticker import ScalarFormatter
import numpy as np
import pandas as pd
from scipy.stats import linregress

from fair.energy_balance_model import EnergyBalanceModel

here = os.path.dirname(os.path.realpath(__file__))

os.makedirs(os.path.join(here, '..', 'figures'), exist_ok=True)

ensemble_size=1001

df_configs = pd.read_csv(os.path.join(here, '..', 'data_input', 'fair-2.1.0', 'calibrated_constrained_parameters.csv'), index_col=0)
configs = df_configs.index

df_aerosol = pd.read_csv(os.path.join(here, '..', 'data_output', 'climate_configs', f'aerosol_forcing_2014.csv'), index_col=0)

ecs = np.zeros(1001)
tcr = np.zeros(1001)

for i, config in enumerate(configs):
    ebm = EnergyBalanceModel(
        ocean_heat_capacity = df_configs.loc[config, 'c1':'c3'],
        ocean_heat_transfer = df_configs.loc[config, 'kappa1':'kappa3'],
        deep_ocean_efficacy = df_configs.loc[config, 'epsilon'],
        gamma_autocorrelation = df_configs.loc[config, 'gamma'],
        forcing_4co2 = df_configs.loc[config, 'F_4xCO2'],
        timestep=3,
        stochastic_run=False,
    )
    ebm.emergent_parameters()
    ecs[i], tcr[i] = (ebm.ecs, ebm.tcr)

pl.rcParams['figure.figsize'] = (17.8/2.54, 6.0/2.54)
pl.rcParams['font.size'] = 7 #20
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

outputs = {}

for scenario in ['dice', 'dice_below2deg', 'dice_1p5deglowOS']:
    outputs[scenario] = {}
    df = pd.read_csv(os.path.join(here, '..', 'data_output', 'results', f'{scenario}__social_cost_of_carbon.csv'), index_col=0)
    outputs[scenario]['social_cost_of_carbon'] = df[:].T.values[0, :]
    df = pd.read_csv(os.path.join(here, '..', 'data_output', 'results', f'{scenario}__temperature.csv'), index_col=0)
    outputs[scenario]['temperature_2050'] = df[:].T.values[9, :]
    df = pd.read_csv(os.path.join(here, '..', 'data_output', 'results', f'{scenario}__CO2_total_emissions.csv'), index_col=0)
    outputs[scenario]['CO2_total_emissions_2050'] = df[:].T.values[9, :]

labels = {
    'dice': "'Optimal'",
    'dice_below2deg': "2°C",
    'dice_1p5deglowOS': "1.5°C"
}

colors = {
    'dice': "#003f5c",
    'dice_below2deg': "#bc5090",
    'dice_1p5deglowOS': "#ffa600"
}

fig, ax = pl.subplots(1, 3)
for scenario in ['dice', 'dice_below2deg', 'dice_1p5deglowOS']:
    ax[0].scatter(ecs, outputs[scenario]['social_cost_of_carbon'], alpha=0.3, label=labels[scenario], color=colors[scenario])
    lr = linregress(ecs, outputs[scenario]['social_cost_of_carbon'])
    print(lr)
    #ax[0].plot(np.linspace(1.4, 7.5), lr.slope*np.linspace(1.4, 7.5) + lr.intercept, color='k')
ax[0].set_yscale('log')
ax[0].set_xlim(1, 8)
ax[0].set_ylim(5, 12000)
ax[0].set_title("(a) ECS v SCC")
ax[0].set_ylabel("Social cost of carbon, 2020\$")
ax[0].set_xlabel("ECS, °C")
ax[0].yaxis.set_major_formatter(ScalarFormatter())

for scenario in ['dice', 'dice_below2deg', 'dice_1p5deglowOS']:
    ax[1].scatter(ecs, outputs[scenario]['CO2_total_emissions_2050'], alpha=0.3, label=labels[scenario], color=colors[scenario])
    lr = linregress(ecs, outputs[scenario]['CO2_total_emissions_2050'])
    print(lr)
    #ax.plot(np.linspace(1.4, 7.5), lr.slope*np.linspace(1.4, 7.5) + lr.intercept, color='k')
ax[1].set_xlim(1, 8)
ax[1].set_ylim(-20, 60)
ax[1].set_title("(b) ECS v 2050 CO$_2$ emissions")
ax[1].set_ylabel("Emissions in 2050, Gt CO$_2$ yr$^{-1}$")
ax[1].set_xlabel("ECS, °C")
ax[1].yaxis.set_major_formatter(ScalarFormatter())
#ax[1].legend(frameon=True)
ax[1].text(7.7, 25, "'Optimal'", ha='right', color=colors['dice'], fontweight='bold')
ax[1].text(7.7, 18, "2°C", ha='right', color=colors['dice_below2deg'], fontweight='bold')
ax[1].text(7.7, 11, "1.5°C", ha='right', color=colors['dice_1p5deglowOS'], fontweight='bold')

for scenario in ['dice', 'dice_below2deg', 'dice_1p5deglowOS']:
    ax[2].scatter(df_aerosol.values.squeeze(), outputs[scenario]['social_cost_of_carbon'], alpha=0.3, label=labels[scenario], color=colors[scenario])
    lr = linregress(df_aerosol.values.squeeze(), outputs[scenario]['social_cost_of_carbon'])
    print(lr)
    #ax.plot(np.linspace(1.4, 7.5), lr.slope*np.linspace(1.4, 7.5) + lr.intercept, color='k')
ax[2].set_yscale('log')
ax[2].set_xlim(-2.7, 0.2)
ax[2].set_ylim(5, 12000)
ax[2].set_title("(c) 2014 aerosol ERF v SCC")
ax[2].set_ylabel("Social cost of carbon, 2020\$")
ax[2].set_xlabel("Aerosol ERF in 2014, W m$^{-2}$")
ax[2].yaxis.set_major_formatter(ScalarFormatter())
fig.tight_layout()
pl.savefig(os.path.join(here, '..', 'figures', f'correlations.png'))
pl.savefig(os.path.join(here, '..', 'figures', f'correlations.pdf'))
pl.show()
