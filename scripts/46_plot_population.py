import os

import matplotlib.pyplot as pl
import numpy as np
import pandas as pd

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

pl.plot(np.arange(2020, 2520, 5), data_combined.T)
pl.show()
