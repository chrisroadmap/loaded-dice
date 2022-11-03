import os

import matplotlib.pyplot as pl
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.stats import multivariate_normal

here = os.path.dirname(os.path.realpath(__file__))

df = pd.read_csv(os.path.join(here, '..', 'data_input', 'wg3', 'ar6.3.7.15.csv'))

def fit(x, a, b):
    return a * x**b

p, cov = curve_fit(fit, df.carbon_price[(df.carbon_price>0)&(df.mitigation>0)], df.mitigation[(df.carbon_price>0)&(df.mitigation>0)])
print(p)
print(cov)

draws = multivariate_normal.rvs(p, cov, random_state=826915, size=1001)
print(draws)

pl.scatter(df.carbon_price[(df.carbon_price>0)&(df.mitigation>0)], df.mitigation[(df.carbon_price>0)&(df.mitigation>0)])
xrange = np.linspace(0, df.carbon_price.max())
pl.plot(xrange, fit(xrange, *p))
for i in range(1001):
    pl.plot(xrange, fit(xrange, *draws[i, :]), color='k', lw=1, alpha=0.2)
pl.show()
