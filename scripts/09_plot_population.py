import os

import matplotlib.pyplot as pl
from matplotlib.ticker import StrMethodFormatter
import numpy as np
import pandas as pd

pl.rcParams['figure.figsize'] = (9/2.54, 9/2.54)
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

here = os.path.dirname(os.path.realpath(__file__))

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

ax.semilogy(np.arange(2020, 2520, 5), data_combined.T/1e6, zorder=-7)
ax.set_ylabel('Population (billions)')
ax.set_xlim(2020, 2515)
ax.yaxis.set_major_formatter(StrMethodFormatter("{x:g}"))
ax.set_ylim(0.1, 300)
ax.set_title('Population projections')


fig.tight_layout()
pl.savefig(os.path.join(here, '..', 'figures', 'population.png'))
pl.savefig(os.path.join(here, '..', 'figures', 'population.pdf'))

pl.show()
