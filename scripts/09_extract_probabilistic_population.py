import os
from tqdm import tqdm
import pathlib

import numpy as np
import pooch
import pyarrow.feather as feather
import pandas as pd
import py7zr
import shutil

here = os.path.dirname(os.path.realpath(__file__))

zipfile = pooch.retrieve(
    "https://zenodo.org/record/6016583/files/rffsps_v5.7z",
    known_hash = "md5:0045d02f72bbc08db9fbdee713bf4633",
    progressbar=True,
)

target = pathlib.Path(os.path.join(here, '..', 'data_input', 'rff_population_gdp')).resolve()

with py7zr.SevenZipFile(zipfile, mode='r') as z:
    extract_files = [file for file in z.getnames() if 'pop_income/' in file]
    z.extract(path=target, targets=extract_files)

data = np.ones((57, 10000)) * np.nan
for run in tqdm(range(1, 10001)):
    df = feather.read_feather(os.path.join(here, '..', 'data_input', 'rff_population_gdp', 'pop_income', f'rffsp_pop_income_run_{run}.feather'))
    for period, year in enumerate(range(2020, 2305, 5)):
        data[period, run-1] = df[df.Year==year].Pop.sum()

df_out = pd.DataFrame(data.T, columns=range(2020, 2305, 5), index=range(1, 10001))
df_out.to_csv(os.path.join(here, '..', 'data_input', 'rff_population_gdp', 'population.csv'))

shutil.rmtree(os.path.join(here, '..', 'data_input', 'rff_population_gdp', 'pop_income'))
