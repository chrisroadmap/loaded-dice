# Multiple linear regression of CO2 from AFOLU versus CO2 from FFI and year

import copy
import os

import matplotlib.pyplot as pl
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import linregress

pl.rcParams['figure.figsize'] = (12/2.54, 12/2.54)
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

# just use pandas
ar6 = pd.read_csv(os.path.join(here, "..", "data_input", "wg3", "co2_ffi_afolu_harmonized.csv"))
ar6 = ar6.loc[
    (ar6['variable']=="Emissions|CO2|Energy and Industrial Processes") |
    (ar6['variable']=="Emissions|CO2|AFOLU")
, :]

ar6_edit = copy.deepcopy(ar6)

for item in ar6.groupby(['model','scenario']):
    if len(item[1]) < 2:
        model = item[0][0]
        scenario = item[0][1]
        ar6_edit = ar6_edit.drop(ar6_edit[(ar6_edit['model']==model) & (ar6_edit['scenario']==scenario)].index)

y = np.empty((0))
x = np.empty((0, 2))

for year in range(2020, 2105, 10):
    afolu = ar6_edit.loc[(ar6_edit['variable']=='Emissions|CO2|AFOLU'), str(year)].values/1000
    ffi   = ar6_edit.loc[(ar6_edit['variable']=='Emissions|CO2|Energy and Industrial Processes'), str(year)].values/1000
    period = (year-2020)/5+1 * np.ones_like(ffi)
    y = np.append(y, afolu)
    x = np.append(x, np.column_stack([ffi, period]), axis=0)
    if year>2020:
        pl.scatter(ffi, afolu, label=year)
        sl, ic, _, _, _ = linregress(ffi, afolu)
        pl.plot(ffi, sl*ffi+ic)
#    x = np.append(x, ffi)
pl.legend()
pl.xlabel('CO$_2$ Energy & Industrial processes')
pl.ylabel('CO$_2$ AFOLU')
pl.title('AR6 WG3 IAM Scenarios')
pl.tight_layout()
pl.savefig(os.path.join(here, '..', 'figures', 'co2_ffi_afolu.png'))
pl.savefig(os.path.join(here, '..', 'figures', 'co2_ffi_afolu.pdf'))
pl.show()

x = sm.add_constant(x)
model = sm.OLS(y, x)
results = model.fit()
print(results.summary())

df_out = pd.DataFrame(results.params, index=['constant', 'CO2_EIP', 'period'], columns=['coefficient'])
df_out.to_csv(os.path.join(here, '..', 'data_output', 'climate_configs', 'afolu_regression.csv'))
