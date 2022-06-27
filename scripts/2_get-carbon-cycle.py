# script to grab carbon cycle box parameters from AR6 restart runs.

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
years = np.arange(1750, 2021)

startyear = 1750
first_scenyear = 2015
last_scenyear = 2020
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

emissions_out = np.ones((271, 40)) * np.nan
emissions_out[:,0] = years

years_future = [2015, 2020]
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
        (ssp_df['Variable'].str.endswith(specie)), '2015':'2020'].dropna(axis=1))
    emissions_out[first_row:(last_row+1), i+1] = f(
        np.arange(first_scenyear, last_scenyear+1)
    )*unit_convert[i+1]

# grab configs
with open(os.path.join(here, '..', 'data_input', 'fair-1.6.2', 'fair-1.6.2-wg3-params.json')) as f:
    config_list = json.load(f)

cc_feedbacks=np.zeros((2237, 3))
for i in range(2237):
    cc_feedbacks[i, 0], cc_feedbacks[i, 1], cc_feedbacks[i, 2] = (
        config_list[i]['r0'],
        config_list[i]['rc'],
        config_list[i]['rt']
    )
df = pd.DataFrame(cc_feedbacks, columns=['r0', 'rc', 'rt'])
df.to_csv(os.path.join(here, '..', 'data_output', 'cc-feedbacks.csv'))

# run fair in original impulse response mode for restarts
def _calculate_geoffroy_helper_parameters(
    cmix, cdeep, lambda0, efficacy, eta, f2x
):

    ecs = f2x/lambda0
    tcr = f2x/(lambda0 + efficacy*eta)

    b_pt1 = (lambda0 + efficacy * eta) / cmix
    b_pt2 = eta / cdeep
    b = b_pt1 + b_pt2
    b_star = b_pt1 - b_pt2
    delta = b ** 2 - (4 * lambda0 * eta) / (cmix * cdeep)

    taucoeff = cmix * cdeep / (2 * lambda0 * eta)
    d1 = taucoeff * (b - delta ** 0.5)
    d2 = taucoeff * (b + delta ** 0.5)

    phicoeff = cmix / (2 * efficacy * eta)
    phi1 = phicoeff * (b_star - delta ** 0.5)
    phi2 = phicoeff * (b_star + delta ** 0.5)

    qdenom = cmix * (phi2 - phi1)
    q1 = d1 * phi2 / qdenom
    q2 = -d2 * phi1 / qdenom

    out = {
        "d1": d1,
        "d2": d2,
        "q1": q1,
        "q2": q2,
        "ecs": ecs,
        "tcr": tcr,
    }
    return out

def run_fair(args):
    c, f, t, restart_out = fair.forward.fair_scm(**args)
    return (
        restart_out[0][0],
        restart_out[0][1],
        restart_out[0][2],
        restart_out[0][3]
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
        updated_config[i]['emissions'] = emissions[:266]
        updated_config[i]['diagnostics'] = 'AR6'
        updated_config[i]["efficacy"] = np.ones(45)
        updated_config[i]["gir_carbon_cycle"] = True
        updated_config[i]["temperature_function"] = "Millar"
        updated_config[i]["aerosol_forcing"] = "aerocom+ghan2"
        updated_config[i]["fixPre1850RCP"] = False
        updated_config[i]["restart_out"] = True
        solar_truncated = updated_config[i]["F_solar"][:266]
        updated_config[i]['F_solar'] = solar_truncated
        volcanic_truncated = updated_config[i]["F_volcanic"][:266]
        updated_config[i]['F_volcanic'] = volcanic_truncated
        nat_truncated = updated_config[i]['natural'][:266, :]
        updated_config[i]['natural'] = nat_truncated
        out = _calculate_geoffroy_helper_parameters(
            cfg['ocean_heat_capacity'][0],
            cfg['ocean_heat_capacity'][1],
            cfg['lambda_global'],
            cfg['deep_ocean_efficacy'],
            cfg['ocean_heat_exchange'],
            cfg['F2x']
        )
        updated_config[i]['d'] = np.array([out['d1'], out['d2']])
        updated_config[i]['q'] = np.array([out['q1'], out['q2']])

    cbox = np.ones((len(updated_config), 4)) * np.nan

    for i, cfg in tqdm(enumerate(updated_config), total=len(updated_config), position=0, leave=True):
        cbox[i,0], cbox[i,1], cbox[i,2], cbox[i,3] = run_fair(updated_config[i])

    return cbox * fair.constants.general.ppm_gtc

results_out = fair_process(emissions_out)

df = pd.DataFrame(results_out, columns=['box1', 'box2', 'box3', 'box4'])
df.to_csv(os.path.join(here, '..', 'data_output', 'carbon-boxes.csv'))
