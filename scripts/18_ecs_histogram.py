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

pl.rcParams['figure.figsize'] = (20/2.54, 20/2.54)
pl.rcParams['font.size'] = 20
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
    for variable in ['social_cost_of_carbon']:
        df = pd.read_csv(os.path.join(here, '..', 'data_output', 'results', f'{scenario}__{variable}.csv'), index_col=0)
        outputs[scenario][variable] = df[:].T.values[0, :]

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

fig, ax = pl.subplots(1, 1)
for scenario in ['dice', 'dice_below2deg', 'dice_1p5deglowOS']:
    ax.scatter(ecs, outputs[scenario]['social_cost_of_carbon'], alpha=0.3, label=labels[scenario], color=colors[scenario])
pl.yscale('log')
ax.set_xlim(1, 7)
ax.set_ylim(5, 10000)
ax.set_title("Equilibrium climate sensitivity")
ax.set_ylabel("Social cost of carbon, 2020\$")
ax.set_xlabel("ECS, °C")
ax.yaxis.set_major_formatter(ScalarFormatter())
ax.legend(fontsize=14, frameon=False)
fig.tight_layout()
pl.savefig(os.path.join(here, '..', 'figures', f'ecs_scc.png'))
pl.savefig(os.path.join(here, '..', 'figures', f'ecs_scc.pdf'))
pl.show()

fig, ax = pl.subplots(1, 1)
for scenario in ['dice', 'dice_below2deg', 'dice_1p5deglowOS']:
    ax.scatter(tcr, outputs[scenario]['social_cost_of_carbon'], alpha=0.3, label=labels[scenario], color=colors[scenario])
pl.yscale('log')
ax.set_xlim(0.8, 3.2)
ax.set_ylim(5, 10000)
ax.set_title("Transient climate response")
ax.set_ylabel("Social cost of carbon, 2020\$")
ax.set_xlabel("TCR, °C")
ax.yaxis.set_major_formatter(ScalarFormatter())
ax.legend(fontsize=14, frameon=False)
fig.tight_layout()
pl.savefig(os.path.join(here, '..', 'figures', f'tcr_scc.png'))
pl.savefig(os.path.join(here, '..', 'figures', f'tcr_scc.pdf'))
pl.show()
