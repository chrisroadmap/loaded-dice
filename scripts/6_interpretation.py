import os

import matplotlib.pyplot as pl
import numpy as np
import pandas as pd

here = os.path.dirname(os.path.realpath(__file__))

ensemble_size=2237

dfs = []
for run in range(ensemble_size):
    dfs.append(pd.read_csv(os.path.join(here, "..", "data_output", "dice", f"{run:04d}.csv"), index_col=0))

for run in range(ensemble_size):
    pl.plot(np.arange(2015, 2115, 5), dfs[run].loc['Atmospheric concentrations ppm'][:20])
pl.show()

for run in range(ensemble_size):
    pl.plot(np.arange(2015, 2115, 5), dfs[run].loc['Atmospheric Temperature rel. 1850-1900'][:20])
pl.show()

for run in range(ensemble_size):
    pl.plot(np.arange(2015, 2115, 5), dfs[run].loc['Carbon Price (per t CO2)'][:20])
pl.show()

for run in range(ensemble_size):
    pl.plot(np.arange(2015, 2115, 5), dfs[run].loc['Social cost of carbon'][:20])
pl.show()

scc2020 = np.ones(ensemble_size) * np.nan
for run in range(ensemble_size):
    scc2020[run] = dfs[run].loc['Social cost of carbon'][1]
pl.hist(scc2020)
pl.show()
