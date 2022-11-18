import os

import numpy as np
import pandas as pd

here = os.path.dirname(os.path.realpath(__file__))

ensemble_size=1001

df_configs = pd.read_csv(os.path.join(here, '..', 'data_input', 'fair-2.1.0', 'ar6_calibration_ebm3.csv'), index_col=0)
configs = df_configs.index

outputs = {}
for scenario in ['dice', 'dice_below2deg', 'dice_1p5deglowOS']:
    outputs[scenario] = {}
    for variable in ['interest_rate']:
        df = pd.read_csv(os.path.join(here, '..', 'data_output', 'results', f'{scenario}__{variable}.csv'), index_col=0)
        outputs[scenario][variable] = df[:].T.values

    print(np.nanpercentile(outputs[scenario][variable][0, :], (5, 50, 95)))#*rho[scenario]+eta[scenario])
