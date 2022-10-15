# Multiple linear regression of CO2 from AFOLU versus CO2 from FFI and year

import copy
import os

import matplotlib.pyplot as pl
import numpy as np
import pandas as pd
import statsmodels.api as sm
import scipy.stats as st
import scipy.optimize as op

here = os.path.dirname(os.path.realpath(__file__))

# just use pandas
ar6 = pd.read_csv(os.path.join(here, "..", "data_input", "wg3", "co2_ffi_afolu_harmonized.csv"))
ar6 = ar6.loc[
    (ar6['variable']=="Emissions|CO2|Energy and Industrial Processes") |
    (ar6['variable']=="Emissions|CO2|AFOLU")
, :]
price = pd.read_csv(os.path.join(here, "..", "data_input", "wg3", "co2_ffi_afolu_price.csv"))
price = price.loc[
    (price['Variable']=="Price|Carbon")
, :]

ar6 = pd.concat((ar6, price.rename(columns=str.lower)), axis=0).reset_index(drop=True)
ar6 = ar6.sort_values(['model', 'scenario'])

ar6_edit = copy.deepcopy(ar6)

for item in ar6.groupby(['model','scenario']):
    #print(item[0], len(item[1]))
    if len(item[1]) < 3:
        model = item[0][0]
        scenario = item[0][1]
        #print(item[1])
        #print(len(item[1]), item[0], (ar6_edit[(ar6_edit['model']==model) & (ar6_edit['scenario']==scenario)].index))
        #print(ar6_edit[(ar6_edit['model']==model) & (ar6_edit['scenario']==scenario)].index)
        for index in ar6_edit[(ar6_edit['model']==model) & (ar6_edit['scenario']==scenario)].index:
            ar6_edit = ar6_edit.drop(index)

#ar6_edit.to_csv(os.path.join(here, '..', 'test.csv'))

y = np.empty((0))
x = np.empty((0, 3))

ar6_edit.drop(columns=['2021', '2022', '2023', '2024'], inplace=True)

for item in ar6.groupby(['model','scenario']):
    model = item[0][0]
    scenario = item[0][1]
    if 'base' in scenario.lower() or 'nopolicy' in scenario.lower():
        pl.plot(np.arange(2020, 2101, 5), ar6_edit.loc[
            (ar6_edit['variable']=='Emissions|CO2|AFOLU')&
            (ar6_edit['model']==model)&
            (ar6_edit['scenario']==scenario),
        '2020':'2100'].interpolate(axis=1).T/1000)
pl.show()

pl.plot(np.arange(2020, 2101, 5), ar6_edit.loc[ar6_edit['variable']=='Emissions|CO2|AFOLU', '2020':'2100'].interpolate(axis=1).T/1000)

def polyfit(x, a, b, c, d, e):
    return a*x**4 + b*x**3 + c*x**2 + d*x + e

median = np.median(ar6_edit.loc[ar6_edit['variable']=='Emissions|CO2|AFOLU', '2020':'2100'].interpolate(axis=1).T, axis=1)/1000
median_fit = op.curve_fit(polyfit, np.arange(1, 18), median)
p95 = np.percentile(ar6_edit.loc[ar6_edit['variable']=='Emissions|CO2|AFOLU', '2020':'2100'].interpolate(axis=1).T, 95, axis=1)/1000
p95_fit = op.curve_fit(polyfit, np.arange(1, 18), p95)
p05 = np.percentile(ar6_edit.loc[ar6_edit['variable']=='Emissions|CO2|AFOLU', '2020':'2100'].interpolate(axis=1).T, 5, axis=1)/1000
p05_fit = op.curve_fit(polyfit, np.arange(1, 18), p05)

print(median_fit)

pl.plot(np.arange(2020, 2101, 5), median, color='k')
pl.plot(np.arange(2020, 2101, 5), polyfit(np.arange(1, 18), *median_fit[0]), color='k', ls='--')
pl.plot(np.arange(2020, 2101, 5), p95, color='k')
pl.plot(np.arange(2020, 2101, 5), polyfit(np.arange(1, 18), *p95_fit[0]), color='k', ls='--')
pl.plot(np.arange(2020, 2101, 5), p05, color='k')
pl.plot(np.arange(2020, 2101, 5), polyfit(np.arange(1, 18), *p05_fit[0]), color='k', ls='--')
pl.ylabel('GtCO2/yr')
pl.axhline(0, color='k', ls=':')
pl.title('AR6 IAM scenarios, CO$_2$ AFOLU emissions,\nharmonised & passed vetting')
pl.show()

for year in range(2020, 2101, 10):
    afolu = ar6_edit.loc[(ar6_edit['variable']=='Emissions|CO2|AFOLU'), str(year)].values/1000
    ffi   = ar6_edit.loc[(ar6_edit['variable']=='Emissions|CO2|Energy and Industrial Processes'), str(year)].values/1000
    price = ar6_edit.loc[(ar6_edit['variable']=='Price|Carbon'), str(year)].values
    afolu = afolu[price>0]
    ffi = ffi[price>0]
    price = np.log(price[price>0]) - np.log(26.4307)
    period = (year-2020)/5 * np.ones_like(ffi)

    y = np.append(y, afolu)
    x = np.append(x, np.column_stack([ffi, period, price]), axis=0)
    #sl, ic, _, _, _ = st.linregress(ffi, afolu)
    #pl.scatter(ffi, afolu, label=year)
    #pl.plot(np.linspace(-20, 120), np.linspace(-20, 120) * sl + ic)

#pl.title('AR6 IAM scenarios, harmonised & passed vetting')
#pl.legend()
#pl.xlabel('FFI emissions')
#pl.ylabel('AFOLU emissions')
#pl.show()

from statsmodels.formula.api import ols
sm_df = pd.DataFrame(x, columns=['ffi', 'period', 'price'])
sm_df['afolu'] = y - 3.21
results = ols(formula = "afolu ~ ffi + period + price - 1", data=sm_df).fit()

#x = sm.add_constant(x)
#model = sm.OLS(y, x)
#results = model.fit()
print(results.summary())

df_out = pd.DataFrame(results.params, index=['constant', 'CO2_EIP', 'period', 'log(price)_minus_log(26.4307)'], columns=['coefficient'])
df_out.to_csv(os.path.join(here, '..', 'data_output', 'climate_configs', 'afolu_regression.csv'))

# here is the logistic function that we apply to the land use emissions
xrange=np.arange(1, 101)
k = 0.75
pl.plot(np.arange(2020, 2520, 5), 1 - 1 / (1+np.exp(-1*(xrange-2))))
pl.plot(np.arange(2020, 2520, 5), 1 - 1 / (1+np.exp(-k*(xrange-23))))
pl.xlim(2020, 2160)
pl.show()
