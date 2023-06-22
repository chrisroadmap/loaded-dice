import os

import matplotlib.pyplot as pl
from matplotlib.ticker import StrMethodFormatter
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd

pl.rcParams['figure.figsize'] = (8.7/2.54, 8.7/2.54)
pl.rcParams['font.size'] = 7
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

# Grab Nordhaus' DICE 2016
df_dice2016 = pd.read_csv(os.path.join(here, '..', 'dice2016', 'DICER3-opt.csv'), index_col=0, sep=',', header=4, on_bad_lines='skip')

# Grab Nordhaus' DICE 2023
df_dice2023 = pd.read_csv(os.path.join(here, '..', 'dice2023', 'DICE2022-b-3-17-3.csv'), index_col=0, sep=',', header=7, on_bad_lines='skip')
df_dice2023.rename(columns={x:y for x,y in zip(df_dice2023.columns,range(2020, 2525, 5))}, inplace=True)

df = pd.read_csv(os.path.join(here, '..', 'data_input', 'rff_population_gdp', 'population.csv'), index_col=0)
data = df.loc[1:1001, '2020':'2300'].values

growth = (df.loc[1:1001, '2255':'2300'].values/df.loc[1:1001, '2250':'2295'].values).mean(axis=1)
print(growth)

data_ext = np.ones((1001, 43))
data_ext[:, 0] = growth * data[:, -1]

for period in range(1, 43):
    data_ext[:, period] = data_ext[:, period-1] * ((42-period)/42*growth + period/42)

data_combined = np.concatenate((data, data_ext), axis=1)

fig, ax = pl.subplots()

ax.semilogy(np.arange(2020, 2520, 5), data_combined.T/1e6, zorder=-7, lw=0.5, color='0.7')
ax.semilogy(np.arange(2020, 2520, 5), np.median(data_combined.T/1e6, axis=1), lw=1.5, zorder=-6, color='k')
ax.semilogy(np.arange(2015, 2515, 5), 0.001*df_dice2016.loc['Population', :].values.astype(float), lw=1.5, zorder=-6.3, color='orange')
ax.semilogy(np.arange(2020, 2525, 5), 0.001*df_dice2023.loc['Population', :].values[0,:].astype(float), lw=1.5, zorder=-6.5, color='green')
line_rff_ens = Line2D([0], [0], label='RFF-SPs extended ensemble members', color='0.7')
line_rff_med = Line2D([0], [0], label='RFF-SPs extended median (this study)', color='k')
line_2016 = Line2D([0], [0], label='DICE-2016R', color='orange')
line_2023 = Line2D([0], [0], label='DICE-2023R', color='green')

ax.legend(handles=[line_rff_ens, line_rff_med, line_2023, line_2016], fontsize=6, frameon=False, loc='lower left')

ax.set_ylabel('Population (billions)')
ax.set_xlim(2020, 2500)
ax.yaxis.set_major_formatter(StrMethodFormatter("{x:g}"))
ax.set_ylim(0.1, 300)
ax.set_title('Population projections')


fig.tight_layout()
pl.savefig(os.path.join(here, '..', 'figures', 'population.png'))
pl.savefig(os.path.join(here, '..', 'figures', 'population.pdf'))

pl.show()
