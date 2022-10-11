# Multiple linear regression of CO2 from AFOLU versus CO2 from FFI and year

import copy
import os

import matplotlib.pyplot as pl
import numpy as np
import pandas as pd
import statsmodels.api as sm

here = os.path.dirname(os.path.realpath(__file__))

# just use pandas
ar6 = pd.read_csv(os.path.join(here, "..", "data_input", "wg3", "co2_ffi_afolu.csv"))
ar6 = ar6.loc[
    (ar6['Variable']=="Emissions|CO2|Energy and Industrial Processes") |
    (ar6['Variable']=="Emissions|CO2|AFOLU")
, :]

ar6_edit = copy.deepcopy(ar6)

for item in ar6.groupby(['Model','Scenario']):
    if len(item[1]) < 2:
        model = item[0][0]
        scenario = item[0][1]
        ar6_edit = ar6_edit.drop(ar6_edit[(ar6_edit['Model']==model) & (ar6_edit['Scenario']==scenario)].index)

y = np.empty((0))
x = np.empty((0, 2))

for year in range(2020, 2105, 10):
    afolu = ar6_edit.loc[(ar6_edit['Variable']=='Emissions|CO2|AFOLU'), str(year)].values/1000
    ffi   = ar6_edit.loc[(ar6_edit['Variable']=='Emissions|CO2|Energy and Industrial Processes'), str(year)].values/1000
    period = (year-2015)/5+1 * np.ones_like(ffi)
    y = np.append(y, afolu)
    x = np.append(x, np.column_stack([ffi, period]), axis=0)
#    x = np.append(x, ffi)

x = sm.add_constant(x)
model = sm.OLS(y, x)
results = model.fit()
print(results.summary())

df_out = pd.DataFrame(results.params, index=['constant', 'CO2_EIP', 'period'], columns=['coefficient'])
df_out.to_csv(os.path.join(here, '..', 'data_output', 'afolu_regression.csv'))

# here is the logistic function that we apply to the land use emissions
xrange=np.arange(1, 101)
k = 0.75
pl.plot(np.arange(2015, 2515, 5), 1 - 1 / (1+np.exp(-k*(xrange-23))))
pl.xlim(2015, 2160)
pl.show()
