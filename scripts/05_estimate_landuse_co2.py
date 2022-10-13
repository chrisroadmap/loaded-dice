# Multiple linear regression of CO2 from AFOLU versus CO2 from FFI and year

import copy
import os

import matplotlib.pyplot as pl
import numpy as np
import pandas as pd
import statsmodels.api as sm
import scipy.stats as st

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

ar6_edit.drop(columns=['2021', '2022', '2023', '2024'], inplace=True)
pl.plot(np.arange(2020, 2101, 5), ar6_edit.loc[ar6_edit['variable']=='Emissions|CO2|AFOLU', '2020':'2100'].interpolate(axis=1).T/1000)
pl.plot(np.arange(2020, 2101, 5), np.median(ar6_edit.loc[ar6_edit['variable']=='Emissions|CO2|AFOLU', '2020':'2100'].interpolate(axis=1).T, axis=1)/1000, color='k')
pl.ylabel('GtCO2/yr')
pl.axhline(0, color='k', ls=':')
pl.title('AR6 IAM scenarios, CO$_2$ AFOLU emissions,\nharmonised & passed vetting')
pl.show()

for year in range(2030, 2101, 10):
    afolu = ar6_edit.loc[(ar6_edit['variable']=='Emissions|CO2|AFOLU'), str(year)].values/1000
    ffi   = ar6_edit.loc[(ar6_edit['variable']=='Emissions|CO2|Energy and Industrial Processes'), str(year)].values/1000
    period = (year-2020)/5+1 * np.ones_like(ffi)
    y = np.append(y, afolu)
    x = np.append(x, np.column_stack([ffi, period]), axis=0)
    sl, ic, _, _, _ = st.linregress(ffi, afolu)
    pl.scatter(ffi, afolu, label=year)
    pl.plot(np.linspace(-20, 120), np.linspace(-20, 120) * sl + ic)

pl.title('AR6 IAM scenarios, harmonised & passed vetting')
pl.legend()
pl.xlabel('FFI emissions')
pl.ylabel('AFOLU emissions')
pl.show()

x = sm.add_constant(x)
model = sm.OLS(y, x)
results = model.fit()
print(results.summary())

df_out = pd.DataFrame(results.params, index=['constant', 'CO2_EIP', 'period'], columns=['coefficient'])
df_out.to_csv(os.path.join(here, '..', 'data_output', 'climate_configs', 'afolu_regression.csv'))

# here is the logistic function that we apply to the land use emissions
xrange=np.arange(1, 101)
k = 0.75
pl.plot(np.arange(2020, 2520, 5), 1 - 1 / (1+np.exp(-1*(xrange-2))))
pl.plot(np.arange(2020, 2520, 5), 1 - 1 / (1+np.exp(-k*(xrange-23))))
pl.xlim(2020, 2160)
pl.show()
