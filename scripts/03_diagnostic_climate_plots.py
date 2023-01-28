import os

import matplotlib.pyplot as pl
import numpy as np
import pandas as pd

pl.rcParams['figure.figsize'] = (17.8/2.54, 8.9/2.54)
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

# data source: https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_gl.txt
# accessed: 2023-01-19
# method: extrapolate the growth rate over last 12 months from Oct21 to Oct22
# add 2.5 months to Oct 2022 (assumed mid-month) to estimate turn of year 2023
co2_20230101_noaa = 418.27
print(co2_20230101_noaa)

ar6_gmst = pd.read_csv(os.path.join(here, '..', 'data_input', 'wg1', 'AR6_GMST.csv'), index_col=0)
years_obs = np.array(ar6_gmst.index, dtype=float)

# weights_19952014 = np.ones(9)
# weights_19952014[0] = 1/6
# weights_19952014[-1] = 1/6

fig, ax = pl.subplots(1,2)
data = pd.read_csv(os.path.join(here, '..', 'data_output', 'climate_configs', f'temperature_historical_ssp245.csv'), index_col=0)
years = np.array(data.columns, dtype=int)
ax[0].fill_between(years, np.percentile(data.T, 5, axis=1), np.percentile(data.T, 95, axis=1), label="FaIR 90% range")
ax[0].plot(years, np.median(data.T, axis=1), color='k', label="FaIR median")
ax[0].plot(years_obs+0.5, ar6_gmst['gmst'], color='r', label="IPCC AR6 best estimate")
ax[0].set_title("Historical warming")
ax[0].set_ylabel("°C relative to 1850-1900")
ax[0].set_xlabel('Year')
ax[0].set_xlim(1850, 2023)
ax[0].set_ylim(-.3, 1.5)
ax[0].legend()

data = pd.read_csv(os.path.join(here, '..', 'data_output', 'climate_configs', 'gas_partitions_ssp245.csv'))
hgdata = ax[1].hist(data['co2_2023'], bins=np.arange(np.floor(np.min(data['co2_2023'])), np.ceil(np.max(data['co2_2023']))+0.5, 0.5), label="FaIR")
ax[1].axvline(co2_20230101_noaa, color='r', label="NOAA")
ax[1].set_title("CO$_2$ concentration, start of 2023")
ax[1].set_xlabel('ppm')
ax[1].set_ylabel('Count')
ax[1].set_ylim(0, 10*np.ceil(np.max(hgdata[0]/10)))
ax[1].set_xlim(np.min(hgdata[1]), np.max(hgdata[1]))
ax[1].legend(loc="upper left")

fig.tight_layout()

pl.savefig(os.path.join(here, '..', 'figures', 'climate_diagnostics.png'))
pl.savefig(os.path.join(here, '..', 'figures', 'climate_diagnostics.pdf'))
pl.show()
