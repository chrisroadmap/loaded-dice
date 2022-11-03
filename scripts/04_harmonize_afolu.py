import aneris.convenience
import pandas as pd
import matplotlib.pyplot as pl
import numpy as np
from tqdm import tqdm
import scmdata

import warnings
import datetime
import os

here = os.path.dirname(os.path.realpath(__file__))

variables = [
    'Emissions|CO2|Energy and Industrial Processes',
    'Emissions|CO2|AFOLU',
]

times = []
yearfaff = range(1850, 2021)
for year in yearfaff:
    times.append(datetime.datetime(year, 1, 1))

history = scmdata.ScmRun(
    os.path.join(here, "..", "data_input", "global-carbon-project", "gcp_iamc_format.csv"), lowercase_cols=True
).filter(region='World', variable=variables).interpolate(target_times=times).timeseries(time_axis="year")


scenarios = scmdata.ScmRun(
    os.path.join(here, "..", "data_input", "wg3", "co2_ffi_afolu_price.csv"), lowercase_cols=True
).filter(region='World', variable=variables).timeseries(time_axis="year")

overrides = pd.DataFrame(
    [
        {
            "method": "reduce_ratio_2080",  # always ratio method by choice
            "variable": "Emissions|CO2|Energy and Industrial Processes",
        },
        {
            "method": "reduce_offset_2150_cov",
            "variable": "Emissions|CO2|AFOLU",
        }
    ]
)

harmonisation_year = 2020

with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    scenarios_harmonised = [
        aneris.convenience.harmonise_all(
            msdf,
            history=history,
            harmonisation_year=harmonisation_year,
            overrides=overrides,
        )
        for _, msdf in tqdm(scenarios.groupby(["model", "scenario"]))
    ]

scenarios_harmonised = pd.concat(scenarios_harmonised).reset_index()
scenarios_harmonised.to_csv(os.path.join(here, '..', 'data_input', 'wg3', 'co2_ffi_afolu_harmonized.csv'), index=False)
