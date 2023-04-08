import os

import matplotlib.pyplot as pl
import numpy as np
import pandas as pd

from fair import FAIR
from fair.energy_balance_model import EnergyBalanceModel
from fair.io import read_properties
from fair.interface import fill, initialise

pl.rcParams['figure.figsize'] = (8.7/2.54, 8.7/2.54)
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

# show that only varying ECS leads to bad projections

ar6_gmst = pd.read_csv(os.path.join(here, '..', 'data_input', 'wg1', 'AR6_GMST.csv'), index_col=0)
years_obs = np.array(ar6_gmst.index, dtype=float)

scenarios = ['ssp245']

# Solar and volcanic forcing
df_solar = pd.read_csv(os.path.join(here, '..', 'data_input', 'fair-2.1.0', 'solar_erf_timebounds.csv'), index_col=0)
df_volcanic = pd.read_csv(os.path.join(here, '..', 'data_input', 'fair-2.1.0', 'volcanic_ERF_monthly_174701-201912.csv'), index_col=0)

start = 1750
end = 2023
timestep = 3

n_hist = (end-start)//timestep+1

solar_3yr = np.zeros(n_hist)
volcanic_3yr = np.zeros(n_hist)
solar_3yr[0] = df_solar.loc[1750, 'erf']
volcanic_3yr[0] = df_volcanic.loc[(start-3):(start-1/24), 'erf'].mean()
for period in range(1, n_hist-1):
    solar_3yr[period] = df_solar.loc[(start+timestep*period-2):(start+timestep*period), 'erf'].mean()
    volcanic_3yr[period] = df_volcanic.loc[(start+timestep*period-3):(start+timestep*period-1/24), 'erf'].mean()
solar_3yr[n_hist-1] = df_solar.loc[2020:2022, 'erf'].mean()
volcanic_3yr[n_hist-1] = volcanic_3yr[n_hist-2] * 0.7

species, properties = read_properties()
df_configs = pd.read_csv(os.path.join(here, '..', 'data_input', 'fair-2.1.0', 'calibrated_constrained_parameters.csv'), index_col=0)

configs_average = df_configs.median()

ebm = EnergyBalanceModel(
    ocean_heat_capacity = configs_average.loc['c1':'c3'],
    ocean_heat_transfer = configs_average.loc['kappa1':'kappa3'],
    deep_ocean_efficacy = configs_average.loc['epsilon'],
    gamma_autocorrelation = configs_average.loc['gamma'],
    forcing_4co2 = configs_average.loc['F_4xCO2'],
    timestep=3,
    stochastic_run=False,
)
ebm.emergent_parameters()
print(ebm.ecs, ebm.tcr)
print(configs_average.loc['F_4xCO2']/configs_average.loc['kappa1']/2)

kappa1 = {}
kappa1['low'] = configs_average.loc['F_4xCO2']/2/2
kappa1['med'] = configs_average.loc['F_4xCO2']/3/2
kappa1['high'] = configs_average.loc['F_4xCO2']/5/2

trend_shape = np.ones(n_hist)
trend_shape[:n_hist] = np.linspace(0, 1, n_hist)

f = FAIR(ch4_method='Thornhill2021')
f.define_time(start, end, timestep)
f.define_scenarios(scenarios)
f.define_configs(['low', 'med', 'high'])
f.define_species(species, properties)
f.allocate()

f.fill_from_rcmip()

# insert GCP emissions here, overriding RCMIP
# NOTE: the AFOLU emissions I have infilled from 1750-1849, using the constraint that
# 1750-1850 cumulative AFOLU was 30 PgC (GCP, 2022). I used a linear ramp, and it
# looks defensible.
df_co2 = pd.read_csv(os.path.join(here, '..', 'data_input', 'global-carbon-project', 'co2_emissions_1750-2022_prelim.csv'))
co2_ffi = df_co2['fossil emissions including carbonation'].values
co2_afolu = df_co2['land-use change emissions'].values
co2_ffi_3yr = np.zeros(n_hist-1)
co2_afolu_3yr = np.zeros(n_hist-1)
for period in range(n_hist-1):
    co2_afolu_3yr[period] = co2_afolu[(timestep*period):(timestep*period+3)].mean() * 44.009/12.011
    co2_ffi_3yr[period] = co2_ffi[(timestep*period):(timestep*period+3)].mean() * 44.009/12.011

fill(f.emissions, co2_ffi_3yr[:, None, None], specie='CO2 FFI')
fill(f.emissions, co2_afolu_3yr[:, None, None], specie='CO2 AFOLU')

calibrated_f4co2_mean = df_configs['F_4xCO2'].mean()

fill(f.forcing, volcanic_3yr[:, None, None] * configs_average.loc['scale Volcanic'], specie='Volcanic')
fill(f.forcing,
     solar_3yr[:, None, None] *
     configs_average.loc['solar_amplitude'] +
     trend_shape[:, None, None] * configs_average.loc['solar_trend'],
     specie='Solar'
)

# climate response
for config in ['low', 'med', 'high']:
    kap = np.zeros(3)
    kap[1:] = configs_average.loc['kappa2':'kappa3'].values
    kap[0] = kappa1[config]
    print(kap)
    fill(f.climate_configs['ocean_heat_transfer'], kap, config=config)
fill(f.climate_configs['ocean_heat_capacity'], configs_average.loc['c1':'c3'].values)
fill(f.climate_configs['deep_ocean_efficacy'], configs_average.loc['epsilon'])
fill(f.climate_configs['gamma_autocorrelation'], configs_average.loc['gamma'])
fill(f.climate_configs['sigma_eta'], configs_average.loc['sigma_eta'])
fill(f.climate_configs['sigma_xi'], configs_average.loc['sigma_xi'])
fill(f.climate_configs['stochastic_run'], False)
fill(f.climate_configs['use_seed'], False)
fill(f.climate_configs['forcing_4co2'], configs_average.loc["F_4xCO2"])

# species level
f.fill_species_configs()

# carbon cycle
fill(f.species_configs['iirf_0'], configs_average.loc['r0'], specie='CO2')
fill(f.species_configs['iirf_airborne'], configs_average.loc['rA'], specie='CO2')
fill(f.species_configs['iirf_uptake'], configs_average.loc['rU'], specie='CO2')
fill(f.species_configs['iirf_temperature'], configs_average.loc['rT'], specie='CO2')

# aerosol indirect
fill(f.species_configs['aci_scale'], configs_average.loc['beta'])
fill(f.species_configs['aci_shape'], configs_average.loc['shape Sulfur'], specie='Sulfur')
fill(f.species_configs['aci_shape'], configs_average.loc['shape BC'], specie='BC')
fill(f.species_configs['aci_shape'], configs_average.loc['shape OC'], specie='OC')

# methane lifetime baseline
fill(f.species_configs['unperturbed_lifetime'], 10.11702748, specie='CH4')

# emissions adjustments for N2O and CH4 (we don't want to make these defaults as people might wanna run pulse expts with these gases)
fill(f.species_configs['baseline_emissions'], 19.019783117809567, specie='CH4')
fill(f.species_configs['baseline_emissions'], 0.08602230754, specie='N2O')

# aerosol direct
for specie in ['BC', 'CH4', 'N2O', 'NH3', 'NOx', 'OC', 'Sulfur', 'VOC', 'Equivalent effective stratospheric chlorine']:
    fill(f.species_configs['erfari_radiative_efficiency'], configs_average.loc[f"ari {specie}"], specie=specie)

# forcing
for specie in ['CO2', 'CH4', 'N2O', 'Stratospheric water vapour', 'Contrails', 'Light absorbing particles on snow and ice', 'Land use']:
    fill(f.species_configs['forcing_scale'], configs_average.loc[f"scale {specie}"], specie=specie)
for specie in ['CFC-11', 'CFC-12', 'CFC-113', 'CFC-114', 'CFC-115', 'HCFC-22', 'HCFC-141b', 'HCFC-142b',
    'CCl4', 'CHCl3', 'CH2Cl2', 'CH3Cl', 'CH3CCl3', 'CH3Br', 'Halon-1211', 'Halon-1301', 'Halon-2402',
    'CF4', 'C2F6', 'C3F8', 'c-C4F8', 'C4F10', 'C5F12', 'C6F14', 'C7F16', 'C8F18', 'NF3', 'SF6', 'SO2F2',
    'HFC-125', 'HFC-134a', 'HFC-143a', 'HFC-152a', 'HFC-227ea', 'HFC-23', 'HFC-236fa', 'HFC-245fa', 'HFC-32',
    'HFC-365mfc', 'HFC-4310mee']:
    fill(f.species_configs['forcing_scale'], configs_average.loc['scale minorGHG'], specie=specie)

# ozone
for specie in ['CH4', 'N2O', 'CO', 'NOx', 'VOC', 'Equivalent effective stratospheric chlorine']:
    fill(f.species_configs['ozone_radiative_efficiency'], configs_average.loc[f"o3 {specie}"], specie=specie)

# tune down volcanic efficacy
fill(f.species_configs['forcing_efficacy'], 0.6, specie='Volcanic')


# initial condition of CO2 concentration (but not baseline for forcing calculations)
fill(f.species_configs['baseline_concentration'], configs_average.loc['co2_concentration_1750'], specie='CO2')

# initial conditions
initialise(f.concentration, f.species_configs['baseline_concentration'])
initialise(f.forcing, 0)
initialise(f.temperature, 0)
initialise(f.cumulative_emissions, 0)
initialise(f.airborne_emissions, 0)

f.run()

weights_18501900 = np.ones(18)
weights_18501900[0] = 1/2
weights_18501900[-1] = 1/6

fig, ax = pl.subplots()
ax.plot(f.timebounds, f.temperature[:, 0, 0, 0]-np.average(f.temperature[33:51, 0, 0, 0], weights=weights_18501900), label="ECS=2°C")
ax.plot(f.timebounds, f.temperature[:, 0, 1, 0]-np.average(f.temperature[33:51, 0, 1, 0], weights=weights_18501900), label="ECS=3°C")
ax.plot(f.timebounds, f.temperature[:, 0, 2, 0]-np.average(f.temperature[33:51, 0, 2, 0], weights=weights_18501900), label="ECS=5°C")
ax.plot(years_obs+0.5, ar6_gmst['gmst'], color='k', label="IPCC AR6 best estimate")
ax.set_title("Historical warming, varying ECS")
ax.set_ylabel("°C relative to 1850-1900")
ax.set_xlabel('Year')
ax.set_xlim(1850, 2023)
ax.set_ylim(-.3, 1.8)
ax.legend()

fig.tight_layout()

pl.savefig(os.path.join(here, '..', 'figures', 'ecs_variation.png'))
pl.savefig(os.path.join(here, '..', 'figures', 'ecs_variation.pdf'))
pl.show()
