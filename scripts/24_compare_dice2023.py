import os

import matplotlib.pyplot as pl
from matplotlib.lines import Line2D
from matplotlib.ticker import ScalarFormatter
from matplotlib.patches import Patch
import numpy as np
import pandas as pd

pl.rcParams['figure.figsize'] = (11.9/2.54, 11.9/2.54)
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

os.makedirs(os.path.join(here, '..', 'figures'), exist_ok=True)

ensemble_size=1001

df_configs = pd.read_csv(os.path.join(here, '..', 'data_input', 'fair-2.1.0', 'calibrated_constrained_parameters.csv'), index_col=0)
configs = df_configs.index

yunit = {
    'CO2_FFI_emissions': 'GtCO$_2$ yr$^{-1}$',
    'CO2_total_emissions': 'GtCO$_2$ yr$^{-1}$',
    'CO2_concentration': 'ppm',
    'temperature': '°C relative to 1850-1900',
    'social_cost_of_carbon': '\$(2020) tCO$_2^{-1}$',
    'radiative_forcing': 'W m$^{-2}$'
}
title = {
    'CO2_FFI_emissions': '(a) CO$_2$ fossil emissions',
    'CO2_total_emissions': '(a) CO$_2$ emissions',
    'CO2_concentration': '(b) CO$_2$ concentrations',
    'temperature': '(c) Surface temperature',
    'social_cost_of_carbon': 'Social cost of carbon',
    'radiative_forcing': '(d) Effective radiative forcing'
}
ylim = {
    'CO2_FFI_emissions': (-20, 55),
    'CO2_total_emissions': (-20, 55),
    'CO2_concentration': (250, 700),
    'temperature': (0.5, 4),
    'social_cost_of_carbon': (0, 4000),
    'radiative_forcing': (0, 7)
}
labels = {
    'dice': "'optimal'",
    'dice_below2deg': "2°C",
    'dice_1p5deglowOS': "1.5°C"
}
colors = {
    'dice': "#003f5c",
    'dice_below2deg': "#bc5090",
    'dice_1p5deglowOS': "#ffa600"
}

outputs = {}

np.set_printoptions(precision=3)

# Grab Nordhaus' DICE 2023
df_dice2023 = pd.read_csv(os.path.join(here, '..', 'dice2023', 'DICE2022-b-3-17-3.csv'), index_col=0, sep=',', header=7, on_bad_lines='skip')
df_dice2023.rename(columns={x:y for x,y in zip(df_dice2023.columns,range(2020, 2525, 5))}, inplace=True)

# Grab Nordhaus' DICE 2016
df_dice2016 = pd.read_csv(os.path.join(here, '..', 'dice2016', 'DICER3-opt.csv'), index_col=0, sep=',', header=4, on_bad_lines='skip')
df_dice2016_2c = pd.read_csv(os.path.join(here, '..', 'dice2016', 'resultslimt20.gms.csv'), index_col=0, sep=',', header=4, on_bad_lines='skip')
df_dice2016_1p5c = pd.read_csv(os.path.join(here, '..', 'dice2016', 'resultslimt15av100.gms.csv'), index_col=0, sep=',', header=4, on_bad_lines='skip')

dice2016 = {}
dice2016['dice'] = {}
dice2016['dice_below2deg'] = {}
dice2016['dice_1p5deglowOS'] = {}
dice2016['dice']['CO2_total_emissions'] = df_dice2016.loc['Total Emissions GTCO2 per year', :].values.astype(float)
dice2016['dice_below2deg']['CO2_total_emissions'] = df_dice2016_2c.loc['Total Emissions GTCO2 per year', :].values.astype(float)
dice2016['dice_1p5deglowOS']['CO2_total_emissions'] = df_dice2016_1p5c.loc['Total Emissions GTCO2 per year', :].values.astype(float)
dice2016['dice']['CO2_concentration'] = df_dice2016.loc['Atmospheric concentration C (ppm)', :].values.astype(float)
dice2016['dice_below2deg']['CO2_concentration'] = df_dice2016_2c.loc['Atmospheric concentration C (ppm)', :].values.astype(float)
dice2016['dice_1p5deglowOS']['CO2_concentration'] = df_dice2016_1p5c.loc['Atmospheric concentration C (ppm)', :].values.astype(float)
dice2016['dice']['temperature'] = df_dice2016.loc['Atmospheric Temperature ', :].values.astype(float)
dice2016['dice_below2deg']['temperature'] = df_dice2016_2c.loc['Atmospheric Temperature ', :].values.astype(float)
dice2016['dice_1p5deglowOS']['temperature'] = df_dice2016_1p5c.loc['Atmospheric Temperature ', :].values.astype(float)
dice2016['dice']['radiative_forcing'] = df_dice2016.loc['Forcings', :].values.astype(float)
dice2016['dice_below2deg']['radiative_forcing'] = df_dice2016_2c.loc['Forcings', :].values.astype(float)
dice2016['dice_1p5deglowOS']['radiative_forcing'] = df_dice2016_1p5c.loc['Forcings', :].values.astype(float)


# the first instance is optimal, second is 2C, third is 1.5C
dice2023 = {}
for iscen, scenario in enumerate(['dice', 'dice_below2deg', 'dice_1p5deglowOS']):
    dice2023[scenario] = {}
    dice2023[scenario]['CO2_total_emissions'] = df_dice2023.loc['Total CO2 Emissions, GTCO2/year', :].values[iscen,:].astype(float)
    dice2023[scenario]['CO2_concentration'] = df_dice2023.loc['Atmospheric concentration C (ppm)', :].values[iscen,:].astype(float)
    dice2023[scenario]['temperature'] = df_dice2023.loc['Atmospheric temperaturer (deg c above preind) ', :].values[iscen,:].astype(float)
    dice2023[scenario]['radiative_forcing'] = df_dice2023.loc['Total forcings w/m2', :].values[iscen,:].astype(float)


for scenario in ['dice', 'dice_below2deg', 'dice_1p5deglowOS']:
    outputs[scenario] = {}
    for variable in ['net_zero_year', 'CO2_concentration', 'temperature', 'social_cost_of_carbon', 'CO2_FFI_emissions', 'CO2_total_emissions', 'radiative_forcing']:
        df = pd.read_csv(os.path.join(here, '..', 'data_output', 'results', f'{scenario}__{variable}.csv'), index_col=0)
        outputs[scenario][variable] = df[:].T.values

fig, ax = pl.subplots(2,2)
for i, variable in enumerate(['CO2_total_emissions', 'CO2_concentration', 'temperature', 'radiative_forcing']):
    for scenario in ['dice', 'dice_below2deg', 'dice_1p5deglowOS']:
        ax[i//2,i%2].fill_between(
            np.arange(2023, 2134, 3),
            np.nanpercentile(outputs[scenario][variable][:37, :], 5, axis=1),
            np.nanpercentile(outputs[scenario][variable][:37, :], 95, axis=1),
            color=colors[scenario],
            alpha=0.2,
            lw=0
        )
        # ax[i//2,i%2].fill_between(
        #     np.arange(2023, 2134, 3),
        #     np.nanpercentile(outputs[scenario][variable][:37, :], 16, axis=1),
        #     np.nanpercentile(outputs[scenario][variable][:37, :], 84, axis=1),
        #     color=colors[scenario],
        #     alpha=0.2,
        #     lw=0
        # )
        ax[i//2,i%2].plot(
            np.arange(2023, 2134, 3),
            np.nanmedian(outputs[scenario][variable][:37, :], axis=1),
            color=colors[scenario],
            label=labels[scenario],
        )
        # DICE2023R
        ax[i//2,i%2].plot(
            np.arange(2020, 2135, 5),
            dice2023[scenario][variable][:23],
            color=colors[scenario],
            ls='--',
        )
        # DICE2016R
        ax[i//2,i%2].plot(
            np.arange(2015, 2135, 5),
            dice2016[scenario][variable][:24],
            color=colors[scenario],
            ls=':',
        )
    ax[i//2,i%2].set_xlim(2015,2125)
    ax[i//2,i%2].set_title(title[variable])
    ax[i//2,i%2].set_ylabel(yunit[variable])
    ax[i//2,i%2].set_ylim(ylim[variable])
    ax[i//2,i%2].set_xticks(np.arange(2025, 2130, 25))
    ax[i//2,i%2].axhline(0, ls=':', color='k')
    #ax[i//2,i%2].axvline(2100, ls=':', color='k')
ax[1,1].legend(fontsize=6, frameon=False, loc='upper left')

line_this = Line2D([0], [0], label='this study (median)', color='k')
u90_this = Patch(facecolor='k', lw=0, alpha=0.2, label='this study (5-95% range)')
line_2023 = Line2D([0], [0], label='DICE2023', color='k', ls='--')
line_2016 = Line2D([0], [0], label='DICE2016', color='k', ls=':')
ax[1,0].legend(handles=[line_this, u90_this, line_2023, line_2016], fontsize=6, frameon=False, loc='upper left')

fig.tight_layout()

pl.savefig(os.path.join(here, '..', 'figures', f'compare_dice2023_2016.png'))
pl.savefig(os.path.join(here, '..', 'figures', f'compare_dice2023_2016.pdf'))
pl.show()
