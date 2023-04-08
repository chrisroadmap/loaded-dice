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
# I don't like scmdata's default conversion, so hack
#history["units"] = "Gt CO2/yr"
history = history * 44.009/12.011
arrays = []
for idx in range(0, len(history.index)):
    arrays.append(list(history.index[idx]))
    arrays[-1][3] = "GtCO2/yr"
new_index = pd.MultiIndex.from_tuples(list(zip(*list(map(list,zip(*arrays))))), names=history.index.names)
history.index = new_index

scenarios = scmdata.ScmRun(
    os.path.join(here, "..", "data_input", "wg3", "co2_ffi_afolu_price.csv"), lowercase_cols=True
).filter(region='World', variable=variables).timeseries(time_axis="year")
scenarios = scenarios / 1000
arrays = []
for idx in range(0, len(scenarios.index)):
    arrays.append(list(scenarios.index[idx]))
    arrays[-1][3] = "GtCO2/yr"
new_index = pd.MultiIndex.from_tuples(list(zip(*list(map(list,zip(*arrays))))), names=scenarios.index.names)
scenarios.index = new_index


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

harmonisation_year = 2010

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
