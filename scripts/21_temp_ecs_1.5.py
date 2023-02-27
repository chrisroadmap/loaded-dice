import os

import matplotlib.pyplot as pl
from matplotlib.ticker import ScalarFormatter
import numpy as np
import pandas as pd

from fair.energy_balance_model import EnergyBalanceModel

here = os.path.dirname(os.path.realpath(__file__))

os.makedirs(os.path.join(here, '..', 'figures'), exist_ok=True)

ensemble_size=1001

df_configs = pd.read_csv(os.path.join(here, '..', 'data_input', 'fair-2.1.0', 'calibrated_constrained_parameters.csv'), index_col=0)
configs = df_configs.index

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

outputs = {}

for scenario in ['dice_1p5deglowOS']:
    outputs[scenario] = {}
    for variable in ['temperature']:
        df = pd.read_csv(os.path.join(here, '..', 'data_output', 'results', f'{scenario}__{variable}.csv'), index_col=0)
        outputs[scenario][variable] = df[:].T.values

    peak_temp = np.max(outputs[scenario]['temperature'], axis=0)  # peak temperature

#    print(outputs)

out1 = np.histogram(ecs, bins=np.arange(1, 8, 0.5))
out2 = np.histogram(ecs[peak_temp<=1.5], bins=np.arange(1, 8, 0.5))
print(out1[0])
print(out2[0])
print(out1[0]/out1[0])
print(out2[0]/out1[0])
pl.stairs(100*out1[0]/out1[0], np.arange(1, 8, 0.5), color='0.8', fill=True, label='All scenarios')
pl.stairs(100*out2[0]/out1[0], np.arange(1, 8, 0.5), color="#ffa600", fill=True, label='Peak warming <1.5°C')
pl.xlim(1, 7.5)
pl.ylim(0, 100)
pl.title("Equilibrium climate sensitivity")
pl.ylabel("% of scenarios")
pl.xlabel("ECS, °C")
pl.legend(frameon=True)
pl.tight_layout()
pl.savefig(os.path.join(here, '..', 'figures', f'temp_ecs.png'))
pl.savefig(os.path.join(here, '..', 'figures', f'temp_ecs.pdf'))
pl.show()
