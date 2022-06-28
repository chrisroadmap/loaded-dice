# script to grab non-CO2 forcing from AR6-WG3 runs. We only want anthro.

import json
import os

import fair
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
import scipy.linalg
from tqdm import tqdm

here = os.path.dirname(os.path.realpath(__file__))

# get ssp245
ssp_df = pd.read_csv(os.path.join(here, '..', 'data_input', 'rcmip', 'rcmip-emissions-annual-means-v5-1-0.csv'))
years = np.arange(1750, 2501)

startyear = 1750
first_scenyear = 2015
last_scenyear = 2500
first_row = int(first_scenyear-startyear)
last_row = int(last_scenyear-startyear)

species = [
    '|CO2|MAGICC Fossil and Industrial',
    '|CO2|MAGICC AFOLU',
    '|CH4',
    '|N2O',
    '|Sulfur',
    '|CO',
    '|VOC',
    '|NOx',
    '|BC',
    '|OC',
    '|NH3',
    '|CF4',
    '|C2F6',
    '|C6F14',
    '|HFC23',
    '|HFC32',
    '|HFC4310mee',
    '|HFC125',
    '|HFC134a',
    '|HFC143a',
    '|HFC227ea',
    '|HFC245fa',
    '|SF6',
    '|CFC11',
    '|CFC12',
    '|CFC113',
    '|CFC114',
    '|CFC115',
    '|CCl4',
    '|CH3CCl3',
    '|HCFC22',
    '|HCFC141b',
    '|HCFC142b',
    '|Halon1211',
    '|Halon1202',
    '|Halon1301',
    '|Halon2402',
    '|CH3Br',
    '|CH3Cl',
]

unit_convert = np.ones(40)
unit_convert[1] = 12/44/1000
unit_convert[2] = 12/44/1000
unit_convert[4] = 28/44/1000
unit_convert[5] = 32/64
unit_convert[8] = 14/46

emissions_out = np.ones((751, 40)) * np.nan
emissions_out[:,0] = years

years_future = [2015] + list(range(2020, 2501, 10))
for i, specie in enumerate(species):
    emissions_out[:first_row,i+1] = ssp_df.loc[
        (ssp_df['Model']=='MESSAGE-GLOBIOM')&
        (ssp_df['Region']=='World')&
        (ssp_df['Scenario']=='ssp245')&
        (ssp_df['Variable'].str.endswith(specie)),str(startyear):'2014']*unit_convert[i+1]
    f = interp1d(years_future, ssp_df.loc[
        (ssp_df['Model']=='MESSAGE-GLOBIOM')&
        (ssp_df['Region']=='World')&
        (ssp_df['Scenario']=='ssp245')&
        (ssp_df['Variable'].str.endswith(specie)), '2015':'2500'].dropna(axis=1))
    emissions_out[first_row:(last_row+1), i+1] = f(
        np.arange(first_scenyear, last_scenyear+1)
    )*unit_convert[i+1]

# grab configs
with open(os.path.join(here, '..', 'data_input', 'fair-1.6.2', 'fair-1.6.2-wg3-params.json')) as f:
    config_list = json.load(f)

# run fair in AR6 model
def run_fair(args):
    c, f, t, _, _, _, _ = fair.forward.fair_scm(**args)
    return (
        np.sum(f[:, 1:43], axis=1),
        t[260:271].mean()-t[100:151].mean(),
        t[245:265].mean()-t[100:151].mean()
    )

def fair_process(emissions):
    updated_config = []
    for i, cfg in enumerate(config_list):
        updated_config.append({})
        for key, value in cfg.items():
            if isinstance(value, list):
                updated_config[i][key] = np.asarray(value)
            else:
                updated_config[i][key] = value
        solar = np.zeros(751)
        volcanic = np.zeros(751)
        natural = np.zeros((751, 2))
        updated_config[i]['emissions'] = emissions
        updated_config[i]['diagnostics'] = 'AR6'
        updated_config[i]["efficacy"] = np.ones(45)
        updated_config[i]["gir_carbon_cycle"] = True
        updated_config[i]["temperature_function"] = "Geoffroy"
        updated_config[i]["aerosol_forcing"] = "aerocom+ghan2"
        updated_config[i]["fixPre1850RCP"] = False
        solar[:361] = updated_config[i]["F_solar"]
        updated_config[i]['F_solar'] = solar
        volcanic[:361] = updated_config[i]["F_volcanic"]
        updated_config[i]['F_volcanic'] = volcanic
        natural[:361, :] = updated_config[i]['natural']
        natural[361:, :] = natural[360, :]
        updated_config[i]['natural'] = natural

    f = np.ones((100, len(updated_config))) * np.nan
    t2015 = np.ones(len(updated_config)) * np.nan
    t2005 = np.ones(len(updated_config)) * np.nan

    for i, cfg in tqdm(enumerate(updated_config), total=len(updated_config), position=0, leave=True):
        f_this, t2015[i], t2005[i] = run_fair(updated_config[i])
        for ij, j in enumerate(range(263, 751, 5)):
            f[ij, i] = np.mean(f_this[j:j+5])
            f[98:, i] = f[97, i]

    return (f, t2015, t2005)

f, t2015, t2005 = fair_process(emissions_out)

df = pd.DataFrame(f, index=range(2015, 2515, 5))
df.to_csv(os.path.join(here, '..', 'data_output', 'anthropogenic-non-co2-forcing.csv'))

# rescale the warming to IPCC assessment of 0.85. We want to retain the
# uncertainty structure however, so we will subtract a constant offset.
t2005_mean = np.nanmean(t2005)

df = pd.DataFrame(t2015 - (t2005_mean - 0.85), columns=['surface_warming_2015'])
df.to_csv(os.path.join(here, '..', 'data_output', 'temperature.csv'))
