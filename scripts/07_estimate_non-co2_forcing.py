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

ar6 = pd.read_csv(os.path.join(here, "..", "data_input", "wg3", "co2_total_forcing_fair1.6.2_p05_50_95.csv"))

ar6_05 = ar6.loc[
    (ar6['Variable']=="AR6 climate diagnostics|Effective Radiative Forcing|CO2|FaIRv1.6.2|50.0th Percentile") |
    (ar6['Variable']=="AR6 climate diagnostics|Effective Radiative Forcing|FaIRv1.6.2|5.0th Percentile")
, :]

ar6_50 = ar6.loc[
    (ar6['Variable']=="AR6 climate diagnostics|Effective Radiative Forcing|CO2|FaIRv1.6.2|50.0th Percentile") |
    (ar6['Variable']=="AR6 climate diagnostics|Effective Radiative Forcing|FaIRv1.6.2|50.0th Percentile")
, :]

ar6_95 = ar6.loc[
    (ar6['Variable']=="AR6 climate diagnostics|Effective Radiative Forcing|CO2|FaIRv1.6.2|50.0th Percentile") |
    (ar6['Variable']=="AR6 climate diagnostics|Effective Radiative Forcing|FaIRv1.6.2|95.0th Percentile")
, :]

co2 = pd.read_csv(os.path.join(here, "..", "data_input", "wg3", "co2_ffi_afolu_harmonized.csv"))
co2 = co2.loc[
    (co2['variable']=="Emissions|CO2|Energy and Industrial Processes")
, :]

ar6_05 = pd.concat((ar6_05.rename(columns=str.lower), co2), axis=0).reset_index(drop=True)
ar6_05 = ar6_05.sort_values(['model', 'scenario'])

ar6_50 = pd.concat((ar6_50.rename(columns=str.lower), co2), axis=0).reset_index(drop=True)
ar6_50 = ar6_50.sort_values(['model', 'scenario'])

ar6_95 = pd.concat((ar6_95.rename(columns=str.lower), co2), axis=0).reset_index(drop=True)
ar6_95 = ar6_95.sort_values(['model', 'scenario'])

print(ar6_05.shape, ar6_50.shape, ar6_95.shape)

ar6_05_edit = copy.deepcopy(ar6_05)
for item in ar6_05.groupby(['model','scenario']):
    if len(item[1]) < 3:
        model = item[0][0]
        scenario = item[0][1]
        for index in ar6_05_edit[(ar6_05_edit['model']==model) & (ar6_05_edit['scenario']==scenario)].index:
            ar6_05_edit = ar6_05_edit.drop(index)

ar6_50_edit = copy.deepcopy(ar6_50)
for item in ar6_50.groupby(['model','scenario']):
    if len(item[1]) < 3:
        model = item[0][0]
        scenario = item[0][1]
        for index in ar6_50_edit[(ar6_50_edit['model']==model) & (ar6_50_edit['scenario']==scenario)].index:
            ar6_50_edit = ar6_50_edit.drop(index)

ar6_95_edit = copy.deepcopy(ar6_95)
for item in ar6_95.groupby(['model','scenario']):
    if len(item[1]) < 3:
        model = item[0][0]
        scenario = item[0][1]
        for index in ar6_95_edit[(ar6_95_edit['model']==model) & (ar6_95_edit['scenario']==scenario)].index:
            ar6_95_edit = ar6_95_edit.drop(index)

ar6_05_edit.drop(columns=['region', 'unit'], inplace=True)
ar6_50_edit.drop(columns=['region', 'unit'], inplace=True)
ar6_95_edit.drop(columns=['region', 'unit'], inplace=True)

print(ar6_05_edit)


ar6_05_edit = pd.concat(
    [
        ar6_05_edit.set_index(["model", "scenario", "variable"])
            .groupby(["model", "scenario"])
            .apply(lambda x: x.iloc[1] - x.iloc[0])
            .assign(variable="AR6 climate diagnostics|Effective Radiative Forcing|Non-CO2|FaIRv1.6.2|5.0th Percentile")
            .set_index("variable", append=True),
        ar6_05_edit.set_index(["model", "scenario", "variable"])
    ]
).reset_index()
ar6_50_edit = pd.concat(
    [
        ar6_50_edit.set_index(["model", "scenario", "variable"])
            .groupby(["model", "scenario"])
            .apply(lambda x: x.iloc[1] - x.iloc[0])
            .assign(variable="AR6 climate diagnostics|Effective Radiative Forcing|Non-CO2|FaIRv1.6.2|50.0th Percentile")
            .set_index("variable", append=True),
        ar6_50_edit.set_index(["model", "scenario", "variable"])
    ]
).reset_index()
ar6_95_edit = pd.concat(
    [
        ar6_95_edit.set_index(["model", "scenario", "variable"])
            .groupby(["model", "scenario"])
            .apply(lambda x: x.iloc[1] - x.iloc[0])
            .assign(variable="AR6 climate diagnostics|Effective Radiative Forcing|Non-CO2|FaIRv1.6.2|95.0th Percentile")
            .set_index("variable", append=True),
        ar6_95_edit.set_index(["model", "scenario", "variable"])
    ]
).reset_index()

y = np.empty((0))
x = np.empty((0, 3))

#ar6_edit.drop(columns=['2021', '2022', '2023', '2024'], inplace=True)

non_co2_smoothed_05 = savgol_filter(
    ar6_05_edit.loc[
        ar6_05_edit['variable']=='AR6 climate diagnostics|Effective Radiative Forcing|Non-CO2|FaIRv1.6.2|5.0th Percentile', '2000':'2100'
    ].interpolate(axis=1).T,
    11,
    1,
    axis=0,
#    mode='nearest'
)
non_co2_smoothed_50 = savgol_filter(
    ar6_50_edit.loc[
        ar6_50_edit['variable']=='AR6 climate diagnostics|Effective Radiative Forcing|Non-CO2|FaIRv1.6.2|50.0th Percentile', '2000':'2100'
    ].interpolate(axis=1).T,
    11,
    1,
    axis=0,
#    mode='nearest'
)
non_co2_smoothed_95 = savgol_filter(
    ar6_95_edit.loc[
        ar6_95_edit['variable']=='AR6 climate diagnostics|Effective Radiative Forcing|Non-CO2|FaIRv1.6.2|95.0th Percentile', '2000':'2100'
    ].interpolate(axis=1).T,
    11,
    1,
    axis=0,
#    mode='nearest'
)

pl.plot(
    np.arange(2014, 2101),
    non_co2_smoothed_05[14:, :],
    color='b',
    alpha=0.1
)
pl.plot(
    np.arange(2014, 2101),
    non_co2_smoothed_50[14:, :],
    color='k',
    alpha=0.1
)
pl.plot(
    np.arange(2014, 2101),
    non_co2_smoothed_95[14:, :],
    color='r',
    alpha=0.1
)

pl.title('AR6 IAM scenarios, harmonised & passed vetting')
pl.ylabel('Non-CO$_2$ forcing, W m$^{-2}$')
pl.xlim(2014, 2100)
pl.tight_layout()
pl.savefig(os.path.join(here, '..', 'figures', 'ar6_non-co2.png'))
pl.savefig(os.path.join(here, '..', 'figures', 'ar6_non-co2.pdf'))
pl.show()

for year in range(2020, 2101, 10):
    nonco2_05 = non_co2_smoothed_05[year-2000, :]
    nonco2_50 = non_co2_smoothed_50[year-2000, :]
    nonco2_95 = non_co2_smoothed_95[year-2000, :]
    ffi       = ar6_50_edit.loc[(ar6_50_edit['variable']=='Emissions|CO2|Energy and Industrial Processes'), str(year)].values/1000
    period    = (year-2015)/5 * np.ones_like(ffi)
    fives     = np.ones_like(ffi) * 5
    fiftys    = np.ones_like(ffi) * 50
    ninetyfives = np.ones_like(ffi) * 95
    y = np.append(y, nonco2_05)
    y = np.append(y, nonco2_50)
    y = np.append(y, nonco2_95)
    x = np.append(x, np.column_stack([ffi, period, fives]), axis=0)
    x = np.append(x, np.column_stack([ffi, period, fiftys]), axis=0)
    x = np.append(x, np.column_stack([ffi, period, ninetyfives]), axis=0)
    if year>2020:
        sl05, ic05, _, _, _ = st.linregress(ffi, nonco2_05)
        sl50, ic50, _, _, _ = st.linregress(ffi, nonco2_50)
        sl95, ic95, _, _, _ = st.linregress(ffi, nonco2_95)
        shade = (2120-year)/100
        pl.scatter(ffi, nonco2_05, color=(0, 0, shade))
        pl.scatter(ffi, nonco2_50, color=(shade, shade, shade))
        pl.scatter(ffi, nonco2_95, color=(shade, 0, 0))
        print(year, sl05, sl50, sl95, ic05, ic50, ic95)
        pl.plot(np.linspace(-20, 120), np.linspace(-20, 120) * sl05 + ic05, color=(0, 0, shade))
        pl.plot(np.linspace(-20, 120), np.linspace(-20, 120) * sl50 + ic50, color=(shade, shade, shade), label=year)
        pl.plot(np.linspace(-20, 120), np.linspace(-20, 120) * sl95 + ic95, color=(shade, 0, 0))

pl.title('AR6 IAM scenarios, harmonised & passed vetting')
pl.xlabel('FFI emissions, GtCO$_2$ yr$^{-1}$')
pl.ylabel('Non-CO$_2$ forcing, W m$^{-2}$')
pl.legend()
pl.tight_layout()
pl.savefig(os.path.join(here, '..', 'figures', 'co2_ffi_non-co2.png'))
pl.savefig(os.path.join(here, '..', 'figures', 'co2_ffi_non-co2.pdf'))
pl.show()

sm_df = pd.DataFrame(x, columns=['ffi', 'period', 'quantile'])
sm_df['nonco2'] = y# - 3.21
results = ols(formula = "nonco2 ~ ffi + period + quantile", data=sm_df).fit()

print(results.summary())

df_out = pd.DataFrame(results.params, index=['Intercept', 'ffi', 'period', 'quantile'], columns=['coefficient'])
df_out.to_csv(os.path.join(here, '..', 'data_output', 'climate_configs', 'nonco2_regression.csv'))
