import os
from tqdm import tqdm

import numpy as np
import pooch
import pyarrow.feather as feather
import pandas as pd
import py7zr

here = os.path.dirname(os.path.realpath(__file__))

zipfile = pooch.retrieve(
    "https://zenodo.org/record/6016583/files/rffsps_v5.7z",
    known_hash = "md5:0045d02f72bbc08db9fbdee713bf4633",
    progressbar=True,
)

with py7zr.SevenZipFile(zipfile, mode='r') as z:
    z.extract(path=os.path.join(here, '..', 'data_input', 'rff_population_gdp'), targets='pop_income')

data = np.ones((57, 10000)) * np.nan
for run in tqdm(range(1, 10001)):
    df = feather.read_feather(os.path.join(here, '..', 'data_input', 'rff_population_gdp', 'rffsp_pop_income_run_{run}.feather'))
    for period, year in enumerate(range(2020, 2305, 5)):
        data[period, run-1] = df[df.Year==year].Pop.sum()

df_out = pd.DataFrame(data.T, columns=range(2020, 2305, 5), index=range(1, 10001))
df_out.to_csv(os.path.join(here, '..', 'data_input', 'rff_population_gdp', 'population.csv'))
