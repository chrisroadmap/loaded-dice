import os

import matplotlib.pyplot as pl
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

# Callahan and Mankin 2022 Sci Adv.:
# Cumulative 1992–2013 losses from anthropogenic extreme heat likely fall between
# $5 trillion and $29.3 trillion globally
# this is only extreme heat - not other damages
# delta T in this time was about 0.8K
# global GDP, cumulative, was about $900tn (but IMF data is not consistent)
# so at 0.8K, heat related damages were in the region of 0.5 to 3.5% of GDP
# at 1.5K, damages expected to be in the range of 0.5% to 4.5% (Swiss Re)

trange = np.arange(0,7.01,0.01)

here = os.path.dirname(os.path.realpath(__file__))

def dice2016(t, a1=0, a2=0.00236, b=2):
    return a1*t + a2*t**b

def dice2016_ds2015(t, a1=0, a2=0.00236, b=2):
    return 1 - 1/(1 + a1*t + a2*t**b)

def weitzman2012_ds2015(t, a1=0, a2=0.00284, acrazy=5.07e-6, bcrazy=6.754):
    return 1 - 1/(1 + a1*t + a2*t**2 + acrazy*t**bcrazy)

def fit_burke(t, a1, a2, b):
    return (t-a1) + a2*t**b

def fit_burke_logistic(t, A, B, C, K, Q, nu):
    return A + (K - A) / ((C+Q*np.exp(-B*t))**(1/nu))

burke = pd.read_csv(os.path.join(here, '..', 'data_input', 'Burke2015', 'fig5d_curve_fit.csv'))
temp = burke['T1']
damfrac = -burke['damfrac']/100

p,cov = curve_fit(fit_burke_logistic, temp, damfrac, maxfev=150000)
print(p)

#print(dice2016(trange))
pl.plot(trange, dice2016(trange), label='DICE2016R original')
pl.plot(trange, dice2016_ds2015(trange), label='DICE2013R per Dietz & Stern (2015)')
pl.plot(trange, weitzman2012_ds2015(trange), label='Weitzman 2012 per Dietz & Stern (2015)')
pl.plot(trange, fit_burke_logistic(trange, *p), label='Burke emulation')
pl.plot(temp, damfrac, label='Burke')
pl.plot(trange, dice2016(trange, a2=0.01145), label='Howard and Sterner (2017) max.')

pl.legend()
pl.ylim(0, 1)
pl.xlim(0, 7)

pl.show()
