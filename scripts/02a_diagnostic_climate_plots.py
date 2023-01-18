import os

import matplotlib.pyplot as pl
import numpy as np
import pandas as pd

here = os.path.dirname(os.path.realpath(__file__))

# data source: https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_annmean_mlo.txt
# accessed: 2023-01-17
# method: extrapolate the growth rate from 2021 to 2022, which we assume are mid-year
# means, and add half this to estimate 2023-01-01 smoothed CO2 concentration

co2_2021_mean_noaa = 416.45
co2_2022_mean_noaa = 418.56
co2_20230101_noaa = co2_2022_mean_noaa + 0.5 * (418.56 - 416.45)
print(co2_20230101_noaa)

ar6_gmst = pd.read_csv(os.path.join(here, '..', 'data_input', 'wg1', 'AR6_GMST.csv'), index_col=0)
years_obs = np.array(ar6_gmst.index, dtype=float)

# weights_19952014 = np.ones(9)
# weights_19952014[0] = 1/6
# weights_19952014[-1] = 1/6

data = pd.read_csv(os.path.join(here, '..', 'data_output', 'climate_configs', f'temperature_historical_ssp245.csv'), index_col=0)
years = np.array(data.columns, dtype=int)
pl.fill_between(years, np.percentile(data.T, 5, axis=1), np.percentile(data.T, 95, axis=1))
pl.plot(years, np.median(data.T, axis=1), color='k')
pl.plot(years_obs+0.5, ar6_gmst['gmst'], color='r')
pl.show()
