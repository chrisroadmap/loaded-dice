# Multiple linear regression of CO2 from AFOLU versus CO2 from FFI and year

import copy
import os

import matplotlib.pyplot as pl
import numpy as np
import pandas as pd
from statsmodels.formula.api import ols
import scipy.stats as st
from scipy.signal import savgol_filter
#import scipy.optimize as op

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

ar6 = pd.read_csv(os.path.join(here, "..", "data_input", "wg3", "co2_ffi_major_ghgs_slcfs.csv"))

ar6 = ar6.loc[
    (ar6['Variable']=="Emissions|CO2|Energy and Industrial Processes") |
#    (ar6['Variable']=="Emissions|Sulfur")
    (ar6['Variable']=="Emissions|CH4")
, :]

ar6_edit = copy.deepcopy(ar6)
for item in ar6.groupby(['Model','Scenario']):
    if len(item[1]) < 2:
        model = item[0][0]
        scenario = item[0][1]
        for index in ar6_edit[(ar6_edit['Model']==model) & (ar6_edit['Scenario']==scenario)].index:
            ar6_edit = ar6_edit.drop(index)

ar6_edit.drop(columns=['Region', 'Unit'], inplace=True)

print(ar6_edit)

y = np.empty(0)
x = np.empty((0, 3))

for year in range(2020, 2101, 10):
    ffi       = ar6_edit.loc[(ar6_edit['Variable']=='Emissions|CO2|Energy and Industrial Processes'), str(year)].values/1000
    #so2       = ar6_edit.loc[(ar6_edit['Variable']=='Emissions|Sulfur'), str(year)].values
    so2       = ar6_edit.loc[(ar6_edit['Variable']=='Emissions|CH4'), str(year)].values
    period    = ((year-2023)/3 + 1) * np.ones_like(ffi)
    period2   = ((year-2023)/3 + 1)**2 * np.ones_like(ffi)
    y = np.append(y, so2)
    x = np.append(x, np.column_stack([ffi, period, period2]), axis=0)
    if year>2020:
        sl, ic, _, _, _ = st.linregress(ffi, so2)
        pl.scatter(ffi, so2, alpha=0.3)
        pl.plot(np.linspace(-20, 120), np.linspace(-20, 120) * sl + ic, label=year)

pl.title('AR6 WG3 IAM Scenarios (n=1202)')
pl.xlabel('FFI emissions, GtCO$_2$ yr$^{-1}$')
pl.ylabel('SO$_2$ emissions, MtSO$_2$ yr$^{-1}$')
pl.legend()
pl.tight_layout()
#pl.savefig(os.path.join(here, '..', 'figures', 'co2_ffi_non-co2.png'))
#pl.savefig(os.path.join(here, '..', 'figures', 'co2_ffi_non-co2.pdf'))
pl.show()

sm_df = pd.DataFrame(x, columns=['ffi', 'period', 'period2'])
sm_df['so2'] = y# - 3.21
results = ols(formula = "so2 ~ ffi + period + period2", data=sm_df).fit()

print(results.summary())

#df_out = pd.DataFrame(results.params, index=['Intercept', 'ffi', 'period', 'quantile'], columns=['coefficient'])
#df_out.to_csv(os.path.join(here, '..', 'data_output', 'climate_configs', 'nonco2_regression.csv'))
