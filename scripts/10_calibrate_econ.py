import numpy as np

# use exact numbers for pop and economics, even if precision is unrealistic, just
# because we're dealing with powers of and it will be quite sensitive

pop_2020 = 7.752698916 # bn. Source: RFF-SP
gdp_2019_intdol2017 = 124.41728  # tn. Source: IMF
cap_2019_intdol2017 = 318.77298  # tn. Source: IMF
int_2019_pppdol2017 = 0.2633286574  # kgCO2/$. Source: World Bank

cpi_inflation_2017_2020 = 1.069735445

elas_cap = 0.3
elas_lab = 0.7

# rearrange Cobb-Douglas to estimate total factor productivity

print("2020$ estimate of global capital: ($tn)", cap_2019_intdol2017 * cpi_inflation_2017_2020)
print("2020$ estimate of global product: ($tn)", gdp_2019_intdol2017 * cpi_inflation_2017_2020)
print("2020$ estimate of total factor productivity:", gdp_2019_intdol2017*cpi_inflation_2017_2020 / ( (pop_2020)**elas_lab * ((cap_2019_intdol2017*cpi_inflation_2017_2020)**elas_cap) ))
print("2020$ estimate of emissions intensity (kgCO2/$):", int_2019_pppdol2017/cpi_inflation_2017_2020)
