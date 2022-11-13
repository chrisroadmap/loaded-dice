import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as pl
from tqdm import tqdm
from scipy.interpolate import interp1d

from fair import FAIR
from fair.io import read_properties
from fair.interface import fill, initialise
from fair.forcing.ghg import meinshausen2020

here = os.path.dirname(os.path.realpath(__file__))
os.makedirs(os.path.join(here, '..', 'data_output', 'climate_configs'), exist_ok=True)


erf_2co2 = meinshausen2020(
    np.array([554.30, 731.41, 273.87]) * np.ones((1, 1, 1, 3)),
    np.array([277.15, 731.41, 273.87]) * np.ones((1, 1, 1, 3)),
    np.array((1.05, 0.86, 1.07)) * np.ones((1, 1, 1, 1)),
    np.ones((1, 1, 1, 3)),
    np.array([True, False, False]),
    np.array([False, True, False]),
    np.array([False, False, True]),
    np.array([False, False, False])
).squeeze()[0]

scenarios = ['ssp119', 'ssp126', 'ssp245', 'ssp370']

# Solar and volcanic forcing
df_natural = pd.read_csv(os.path.join(here, '..', 'data_input', 'wg1', 'natural_erf.csv'), index_col=0)
solar_forcing = df_natural['solar'].loc[1750.5:2023.5].values
volcanic_forcing = df_natural['volcanic'].loc[1750.5:2023.5].values

start = 1750
end = 2023
timestep = 3

n_hist = (end-start)//timestep+1

solar_3yr = np.zeros(n_hist)
volcanic_3yr = np.zeros(n_hist)
solar_3yr[0] = solar_forcing[0]
volcanic_3yr[0] = volcanic_forcing[0]
for period in range(1, n_hist):
    solar_3yr[period] = solar_forcing[(timestep*period-2):(timestep*period+1)].mean()
    volcanic_3yr[period] = volcanic_forcing[(timestep*period-2):(timestep*period+1)].mean()

## future solar forcing amplitude to be zero from 2020
#solar_3yr[54:] = 0

species, properties = read_properties()
df_configs =pd.read_csv(os.path.join(here, '..', 'data_input', 'fair-2.1.0', 'ar6_calibration_ebm3.csv'), index_col=0)
configs = np.array(list(df_configs.index))

trend_shape = np.ones(n_hist)
trend_shape[:n_hist] = np.linspace(0, 1, n_hist)

f = FAIR(ch4_method='Thornhill2021')
f.define_time(start, end, timestep)
f.define_scenarios(scenarios)
f.define_configs(configs)
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

fill(f.forcing, volcanic_3yr[:, None, None] * df_configs.loc[configs, 'scale Volcanic'].values.squeeze(), specie='Volcanic')
fill(f.forcing,
     solar_3yr[:, None, None] *
     df_configs.loc[configs, 'solar_amplitude'].values.squeeze() +
     trend_shape[:, None, None] * df_configs.loc[configs, 'solar_trend'].values.squeeze(),
     specie='Solar'
)

# climate response
fill(f.climate_configs['ocean_heat_capacity'], df_configs.loc[configs, 'c1':'c3'].values)
fill(f.climate_configs['ocean_heat_transfer'], df_configs.loc[configs, 'kappa1':'kappa3'].values)
fill(f.climate_configs['deep_ocean_efficacy'], df_configs.loc[configs, 'epsilon'].values.squeeze())
fill(f.climate_configs['gamma_autocorrelation'], df_configs.loc[configs, 'gamma'].values.squeeze())
fill(f.climate_configs['sigma_eta'], df_configs.loc[configs, 'sigma_eta'].values.squeeze())
fill(f.climate_configs['sigma_xi'], df_configs.loc[configs, 'sigma_xi'].values.squeeze())
fill(f.climate_configs['stochastic_run'], False)
fill(f.climate_configs['use_seed'], False)
fill(f.climate_configs['forcing_4co2'], 2 * erf_2co2 * (1 + 0.561*(calibrated_f4co2_mean - df_configs.loc[configs,'F_4xCO2'])/calibrated_f4co2_mean))

# species level
f.fill_species_configs()

# carbon cycle
# TODO: new batch of configs for GCP. For now, modify r0
fill(f.species_configs['iirf_0'], df_configs.loc[configs, 'r0'].values.squeeze()-1.5, specie='CO2')
fill(f.species_configs['iirf_airborne'], df_configs.loc[configs, 'rA'].values.squeeze(), specie='CO2')
fill(f.species_configs['iirf_uptake'], df_configs.loc[configs, 'rU'].values.squeeze(), specie='CO2')
fill(f.species_configs['iirf_temperature'], df_configs.loc[configs, 'rT'].values.squeeze(), specie='CO2')

# aerosol indirect
fill(f.species_configs['aci_scale'], df_configs.loc[configs, 'beta'].values.squeeze())
fill(f.species_configs['aci_shape'], df_configs.loc[configs, 'shape_so2'].values.squeeze(), specie='Sulfur')
fill(f.species_configs['aci_shape'], df_configs.loc[configs, 'shape_bc'].values.squeeze(), specie='BC')
fill(f.species_configs['aci_shape'], df_configs.loc[configs, 'shape_oc'].values.squeeze(), specie='OC')

# methane lifetime baseline
fill(f.species_configs['unperturbed_lifetime'], 10.4198121, specie='CH4')

# emissions adjustments for N2O and CH4 (we don't want to make these defaults as people might wanna run pulse expts with these gases)
fill(f.species_configs['baseline_emissions'], 19.019783117809567, specie='CH4')
fill(f.species_configs['baseline_emissions'], 0.08602230754, specie='N2O')

# aerosol direct
for specie in ['BC', 'CH4', 'N2O', 'NH3', 'NOx', 'OC', 'Sulfur', 'VOC', 'Equivalent effective stratospheric chlorine']:
    fill(f.species_configs['erfari_radiative_efficiency'], df_configs.loc[configs, f"ari {specie}"], specie=specie)

# forcing
for specie in ['CH4', 'N2O', 'Stratospheric water vapour', 'Contrails', 'Light absorbing particles on snow and ice', 'Land use']:
    fill(f.species_configs['forcing_scale'], df_configs.loc[configs, f"scale {specie}"].values.squeeze(), specie=specie)
for specie in ['CFC-11', 'CFC-12', 'CFC-113', 'CFC-114', 'CFC-115', 'HCFC-22', 'HCFC-141b', 'HCFC-142b',
    'CCl4', 'CHCl3', 'CH2Cl2', 'CH3Cl', 'CH3CCl3', 'CH3Br', 'Halon-1211', 'Halon-1301', 'Halon-2402',
    'CF4', 'C2F6', 'C3F8', 'c-C4F8', 'C4F10', 'C5F12', 'C6F14', 'C7F16', 'C8F18', 'NF3', 'SF6', 'SO2F2',
    'HFC-125', 'HFC-134a', 'HFC-143a', 'HFC-152a', 'HFC-227ea', 'HFC-23', 'HFC-236fa', 'HFC-245fa', 'HFC-32',
    'HFC-365mfc', 'HFC-4310mee']:
    fill(f.species_configs['forcing_scale'], df_configs.loc[configs, 'scale minorGHG'].values.squeeze(), specie=specie)
fill(f.species_configs['forcing_scale'], 1 + 0.561*(calibrated_f4co2_mean - df_configs.loc[configs,'F_4xCO2'].values)/calibrated_f4co2_mean, specie='CO2')

# ozone
for specie in ['CH4', 'N2O', 'CO', 'NOx', 'VOC', 'Equivalent effective stratospheric chlorine']:
    fill(f.species_configs['ozone_radiative_efficiency'], df_configs.loc[configs, f"o3 {specie}"], specie=specie)

# tune down volcanic efficacy
fill(f.species_configs['forcing_efficacy'], 0.6, specie='Volcanic')


# initial condition of CO2 concentration (but not baseline for forcing calculations)
fill(f.species_configs['baseline_concentration'], df_configs.loc[configs, 'co2_concentration_1750'].values.squeeze(), specie='CO2')

# initial conditions
initialise(f.concentration, f.species_configs['baseline_concentration'])
initialise(f.forcing, 0)
initialise(f.temperature, 0)
initialise(f.cumulative_emissions, 0)
initialise(f.airborne_emissions, 0)

f.run()

for i, scenario in enumerate(scenarios):
    df_cc = pd.DataFrame(f.gas_partitions.loc[dict(scenario=scenario, specie='CO2')] * 12.011 / 44.009, columns=['geological', 'slow', 'mid', 'fast'], index=configs)
    df_co2 = pd.DataFrame(f.concentration.loc[dict(scenario=scenario, specie='CO2', timebounds=2023)], columns=['co2_2023'], index=configs)
    df = pd.concat([df_cc, df_co2], axis=1)
    df.to_csv(os.path.join(here, '..', 'data_output', 'climate_configs', f'gas_partitions_{scenario}.csv'))

    # calculate "effective" F2x for translation from Meinshausen formula in FaIR to log formula in DICE
    effective_f2x = f.forcing[-1, i, :, 2] * np.log(2) / np.log(f.concentration[-1, i, :, 2] / f.concentration[0, i, :, 2])
    df = pd.DataFrame(np.array([f.forcing[-1, i, :, 2], effective_f2x]).T, index=configs, columns=['co2_forcing_2023', 'effective_f2x'])
    df.to_csv(os.path.join(here, '..', 'data_output', 'climate_configs', f'co2_forcing_{scenario}.csv'))

    # save non-CO2 forcing in 2023
    df = pd.DataFrame((np.nansum(f.forcing[-1, i, :, :], axis=-1) - f.forcing[-1, i, :, 2] - f.forcing[-3, i, :, 54:56].mean(axis=-1)), index=configs)
    df.to_csv(os.path.join(here, '..', 'data_output', 'climate_configs', f'anthropogenic_non-co2_forcing_{scenario}.csv'))

    # use surface layer 1850-1900 offset; apply same offset to all layers to preserve differences between layers that drives diffusion
    df = pd.DataFrame(f.temperature[-1, i, :, :]-f.temperature[33:50, i, :, 0].mean(axis=0), index=configs, columns=['mixed_layer', 'mid_ocean', 'deep_ocean'])
    df.to_csv(os.path.join(here, '..', 'data_output', 'climate_configs', f'temperature_{scenario}.csv'))
