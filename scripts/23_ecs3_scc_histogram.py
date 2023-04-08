import os

import matplotlib.pyplot as pl
from matplotlib.ticker import ScalarFormatter
import numpy as np
import pandas as pd

from fair.energy_balance_model import EnergyBalanceModel
from fair.forcing.ghg import meinshausen2020

pl.rcParams['figure.figsize'] = (8.7/2.54, 8.7/2.54)
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

here = os.path.dirname(os.path.realpath(__file__))

os.makedirs(os.path.join(here, '..', 'figures'), exist_ok=True)

ensemble_size=1001

df_configs = pd.read_csv(os.path.join(here, '..', 'data_input', 'fair-2.1.0', 'calibrated_constrained_parameters.csv'), index_col=0)
configs = df_configs.index

ecs = np.ones(1001) * np.nan

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
    ecs[i] = ebm.ecs

yunit = {
    'social_cost_of_carbon': '\$(2020) tCO$_2^{-1}$',
}
title = {
    'social_cost_of_carbon': 'Social cost of carbon',
}
labels = {
    'dice': 'DICE-2016R "optimal"',
    'dice_below2deg': "Well-below 2°C",
    'dice_1p5deglowOS': "1.5°C-low overshoot"
}
colors = {
    'dice': "#003f5c",
    'dice_below2deg': "#bc5090",
    'dice_1p5deglowOS': "#ffa600"
}

outputs = {}

np.set_printoptions(precision=3)

for scenario in ['dice', 'dice_below2deg', 'dice_1p5deglowOS']:
    outputs[scenario] = {}
    for variable in ['social_cost_of_carbon']:
        df = pd.read_csv(os.path.join(here, '..', 'data_output', 'results', f'{scenario}__{variable}.csv'), index_col=0)
        outputs[scenario][variable] = df[:].T.values

fig, ax = pl.subplots()
for scenario in ['dice', 'dice_below2deg', 'dice_1p5deglowOS']:
    scc = outputs[scenario]['social_cost_of_carbon'][0, :]
    ax.hist(
        scc[np.logical_and(ecs<=3.1, ecs>=2.9)],
        alpha=0.5,
        label=labels[scenario],
        color=colors[scenario],
        density=True,
        bins=np.logspace(-1, 4, 101),
        log=True
    )
ax.set_xscale('log')
pl.rcParams['xtick.minor.visible'] = True
ax.set_xlim(6, 10000)
ax.set_title("Social cost of carbon in 2023, ECS=3°C")
ax.set_xlabel("(2020\$)")
ax.set_ylabel("Density")
ax.set_yticklabels([])
ax.xaxis.set_major_formatter(ScalarFormatter())

fig.tight_layout()
pl.savefig(os.path.join(here, '..', 'figures', f'ecs3_scc_histogram.png'))
pl.savefig(os.path.join(here, '..', 'figures', f'ecs3_scc_histogram.pdf'))
pl.show()
