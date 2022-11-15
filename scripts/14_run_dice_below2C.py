# TODO: change cumulative emissions to SSP126

import json
import os
import subprocess

from scipy.interpolate import interp1d
import numpy as np
from tqdm import tqdm
import pandas as pd

# should really import these constants from FaIR
carbon_convert = 5.1352 * 12.011 / 28.97

class InfeasibleSolutionError(Exception):
    def __init__(self, run):
        print(f"Infeasible solution in run number {run}.")

here = os.path.dirname(os.path.realpath(__file__))

df_configs = pd.read_csv(os.path.join(here, '..', 'data_input', 'fair-2.1.0', 'ar6_calibration_ebm3.csv'), index_col=0)
configs = df_configs.index

os.makedirs(os.path.join(here, 'gams_scripts'), exist_ok=True)
os.makedirs(os.path.join(here, '..', 'data_output', 'dice_below2deg'), exist_ok=True)

df_nonco2 = pd.read_csv(os.path.join(here, '..', 'data_output', 'climate_configs', 'anthropogenic_non-co2_forcing_future_ssp126.csv'), index_col=0)
df_cbox = pd.read_csv(os.path.join(here, '..', 'data_output', 'climate_configs', 'gas_partitions_ssp126.csv'), index_col=0)
df_cr = pd.read_csv(os.path.join(here, '..', 'data_output', 'climate_configs', 'climate_response_params.csv'), index_col=0)
df_co2 = pd.read_csv(os.path.join(here, '..', 'data_output', 'climate_configs', 'co2_forcing_ssp126.csv'), index_col=0)
df_temp = pd.read_csv(os.path.join(here, '..', 'data_output', 'climate_configs', 'temperature_ssp126.csv'), index_col=0)
df_afolu = pd.read_csv(os.path.join(here, '..', 'data_output', 'climate_configs', 'afolu_regression.csv'), index_col=0)
df_nonco2_reg = pd.read_csv(os.path.join(here, '..', 'data_output', 'climate_configs', 'nonco2_regression.csv'), index_col=0)
#
# order = df_nonco2_reg.loc[:, '0'].argsort()
# ranks = order.argsort()
# quantiles = ranks/10

n_configs = 1001

# Load RFF population scenarios and extend to 2500 using a growth rate that converges to zero
df_pop = pd.read_csv(os.path.join(here, '..', 'data_input', 'rff_population_gdp', 'population.csv'), index_col=0)
data_pop = df_pop.loc[:, '2020':'2300'].values
growth_pop = (df_pop.loc[:, '2255':'2300'].values/df_pop.loc[:, '2250':'2295'].values).mean(axis=1)
data_ext_pop = np.ones((10000, 43))
data_ext_pop[:, 0] = growth_pop * data_pop[:, -1]

for period in range(1, 43):
    data_ext_pop[:, period] = data_ext_pop[:, period-1] * ((42-period)/42*growth_pop + period/42)

population_sample = np.concatenate((data_pop, data_ext_pop), axis=1)/1e6
# then interpolate to 3-year timesteps
pop_years_in = np.arange(2020, 2520, 5)
pop_years_out = np.arange(2023, 2501, 3)

f = interp1d(pop_years_in, population_sample)
population_sample_out = f(pop_years_out)

# In this climate-only experiment, we are not modifying away from the median population projection.
pop = np.median(population_sample_out, axis=0)

afolu_const = df_afolu.loc['constant', 'coefficient']
afolu_ffi = df_afolu.loc['CO2_EIP', 'coefficient']
afolu_period = df_afolu.loc['period', 'coefficient']
nonco2_const = df_nonco2_reg.loc['Intercept', 'coefficient']
nonco2_ffi = df_nonco2_reg.loc['ffi', 'coefficient']
nonco2_period = df_nonco2_reg.loc['period', 'coefficient']
nonco2_quantile = df_nonco2_reg.loc['quantile', 'coefficient']

for run, config in tqdm(enumerate(configs[:n_configs]), total=n_configs):
    t1 = df_temp.loc[config, 'mixed_layer']
    t2 = df_temp.loc[config, 'mid_ocean']
    t3 = df_temp.loc[config, 'deep_ocean']
    cr = df_cr.loc[config].values
    f2x = df_co2.loc[config, 'effective_f2x']
    r0 = df_configs.loc[config, 'r0']
    ru = df_configs.loc[config, 'rU']
    rt = df_configs.loc[config, 'rT']
    ra = df_configs.loc[config, 'rA']
    cbox1 = df_cbox.loc[config, 'geological']
    cbox2 = df_cbox.loc[config, 'slow']
    cbox3 = df_cbox.loc[config, 'mid']
    cbox4 = df_cbox.loc[config, 'fast']
    co2_2023 = df_cbox.loc[config, 'co2_2023']
    co2_1750 = df_configs.loc[config, 'co2_concentration_1750']
    nonco2 = df_nonco2.loc[config, :].values

    template = f'''
$ontext
DICE with FaIR carbon cycle and climate response.

Climate module by Chris Smith, 28 June 2022. Economic model is unmodified from the
beta version of DICE-2016R, by William Nordhaus, and downloaded from
http://www.econ.yale.edu/~nordhaus/homepage/homepage/DICE2016R-091916ap.gms

Version is DICE-2016R-091916ap.gms
$offtext

$title        DICE-2016R-FAIR June 2022

set     t        Time periods (3 years per period)                     /1*160/
        box      Carbon box                                            /1*4/

PARAMETERS
** Availability of fossil fuels
        fosslim  Maximum cumulative extraction fossil fuels (GtC)      /6000/
**Time Step
        tstep    Years per Period                                      /3/
** If optimal control
        ifopt    Indicator where optimized is 1 and base is 0          /1/
** Preferences
        elasmu   Elasticity of marginal utility of consumption         /0.35/
        prstp    Initial rate of social time preference per year       /0.0035/
** Technology and population (updated by CS)
        gama     Capital elasticity in production function             /0.300/
        dk       Depreciation rate on capital (per year)               /0.100/
        q0       Initial world gross output 2020 (trill 2020 USD)      /133.09357438648962/
        k0       Initial capital value 2019                            /341.0027556142761/
        a0       Initial level of total factor productivity            /5.4028103629527156/
        ga0      Initial growth rate for TFP per 3 years               /0.045/
        dela     Decline rate of TFP per 3 years                       /0.003/
        l(t)     /1 {pop[0]}, 2 {pop[1]}, 3 {pop[2]}, 4 {pop[3]}, 5 {pop[4]},
                  6 {pop[5]}, 7 {pop[6]}, 8 {pop[7]}, 9 {pop[8]}, 10 {pop[9]},
                 11 {pop[10]}, 12 {pop[11]}, 13 {pop[12]}, 14 {pop[13]}, 15 {pop[14]},
                 16 {pop[15]}, 17 {pop[16]}, 18 {pop[17]}, 19 {pop[18]}, 20 {pop[19]},
                 21 {pop[20]}, 22 {pop[21]}, 23 {pop[22]}, 24 {pop[23]}, 25 {pop[24]},
                 26 {pop[25]}, 27 {pop[26]}, 28 {pop[27]}, 29 {pop[28]}, 30 {pop[29]},
                 31 {pop[30]}, 32 {pop[31]}, 33 {pop[32]}, 34 {pop[33]}, 35 {pop[34]},
                 36 {pop[35]}, 37 {pop[36]}, 38 {pop[37]}, 39 {pop[38]}, 40 {pop[39]},
                 41 {pop[40]}, 42 {pop[41]}, 43 {pop[42]}, 44 {pop[43]}, 45 {pop[44]},
                 46 {pop[45]}, 47 {pop[46]}, 48 {pop[47]}, 49 {pop[48]}, 50 {pop[49]},
                 51 {pop[50]}, 52 {pop[51]}, 53 {pop[52]}, 54 {pop[53]}, 55 {pop[54]},
                 56 {pop[55]}, 57 {pop[56]}, 58 {pop[57]}, 59 {pop[58]}, 60 {pop[59]},
                 61 {pop[60]}, 62 {pop[61]}, 63 {pop[62]}, 64 {pop[63]}, 65 {pop[64]},
                 66 {pop[65]}, 67 {pop[66]}, 68 {pop[67]}, 69 {pop[68]}, 70 {pop[69]},
                 71 {pop[70]}, 72 {pop[71]}, 73 {pop[72]}, 74 {pop[73]}, 75 {pop[74]},
                 76 {pop[75]}, 77 {pop[76]}, 78 {pop[77]}, 79 {pop[78]}, 80 {pop[79]},
                 81 {pop[80]}, 82 {pop[81]}, 83 {pop[82]}, 84 {pop[83]}, 85 {pop[84]},
                 86 {pop[85]}, 87 {pop[86]}, 88 {pop[87]}, 89 {pop[88]}, 90 {pop[89]},
                 91 {pop[90]}, 92 {pop[91]}, 93 {pop[92]}, 94 {pop[93]}, 95 {pop[94]},
                 96 {pop[95]}, 97 {pop[96]}, 98 {pop[97]}, 99 {pop[98]}, 100 {pop[99]},
                 101 {pop[100]}, 102 {pop[101]}, 103 {pop[102]}, 104 {pop[103]}, 105 {pop[104]},
                 106 {pop[105]}, 107 {pop[106]}, 108 {pop[107]}, 109 {pop[108]}, 110 {pop[109]},
                 111 {pop[110]}, 112 {pop[111]}, 113 {pop[112]}, 114 {pop[113]}, 115 {pop[114]},
                 116 {pop[115]}, 117 {pop[116]}, 118 {pop[117]}, 119 {pop[118]}, 120 {pop[119]},
                 121 {pop[120]}, 122 {pop[121]}, 123 {pop[122]}, 124 {pop[123]}, 125 {pop[124]},
                 126 {pop[125]}, 127 {pop[126]}, 128 {pop[127]}, 129 {pop[128]}, 130 {pop[129]},
                 131 {pop[130]}, 132 {pop[131]}, 133 {pop[132]}, 134 {pop[133]}, 135 {pop[134]},
                 136 {pop[135]}, 137 {pop[136]}, 138 {pop[137]}, 139 {pop[138]}, 140 {pop[139]},
                 141 {pop[140]}, 142 {pop[141]}, 143 {pop[142]}, 144 {pop[143]}, 145 {pop[144]},
                 146 {pop[145]}, 147 {pop[146]}, 148 {pop[147]}, 149 {pop[148]}, 150 {pop[149]},
                 151 {pop[150]}, 152 {pop[151]}, 153 {pop[152]}, 154 {pop[153]}, 155 {pop[154]},
                 156 {pop[155]}, 157 {pop[156]}, 158 {pop[157]}, 159 {pop[158]}, 160 {pop[159]}/
** Emissions parameters
        gsigma1  Initial growth of sigma (per year)                    /-0.0152/
        dsig     Decline rate of decarbonization (per period)          /-0.0006/
        e0       Industrial emissions 2023 (GtCO2 per year)            /36.64/
        miu0     Initial emissions control rate for base case 2023     /0.15/
* Initial Conditions
        co2_2023 Initial concentration in atmosphere 2023 (GtC)        /{co2_2023*carbon_convert}/
        co2_1750 Pre-industrial concentration atmosphere  (GtC)        /{co2_1750*carbon_convert}/
* These are for declaration and are defined later
        sig0     Carbon intensity 2023 (kgCO2 per output 2020 Int$)
** Climate model parameters
        g0       Carbon cycle parameter (Leach et al. 2021)
        g1       Carbon cycle parameter (Leach et al. 2021)
        r0       Pre-industrial time-integrated airborne fraction      /{r0}/
        ru       Sensitivity of airborne fraction with CO2 uptake      /{ru}/
        rt       Sensitivity of airborne fraction with temperature     /{rt}/
        ra       Sensitivity of airborne fraction with CO2 airborne    /{ra}/
        tau(box) Lifetimes of the four atmospheric carbon boxes
                     / 1 1e9, 2 394.4, 3 36.54, 4 4.304 /
        a(box)   Partition fraction of the four atmospheric carbon boxes
                     / 1 0.2173, 2 0.2240, 3 0.2824, 4 0.2763 /
        ICBOX1   Initial GtC concentration of carbon box 1 in 2023     /{cbox1}/
        ICBOX2   Initial GtC concentration of carbon box 2 in 2023     /{cbox2}/
        ICBOX3   Initial GtC concentration of carbon box 3 in 2023     /{cbox3}/
        ICBOX4   Initial GtC concentration of carbon box 4 in 2023     /{cbox4}/
        iirf_horizon Time horizon for IIRF in yr                       /100/
        t1_0     three-layer "mixed layer" temperature change          /{t1}/
        t2_0     three-layer "mid-ocean" temperature change            /{t2}/
        t3_0     three-layer "deep-ocean" temperature change           /{t3}/
        EBM_A11  Fast component of mixed layer temperature             /{cr[0]}/
        EBM_A12  Intermediate component of mixed layer temperature     /{cr[1]}/
        EBM_A13  Slow component of mixed layer temperature             /{cr[2]}/
        EBM_A21  Fast component of mid ocean temperature               /{cr[3]}/
        EBM_A22  Intermediate component of mid ocean temperature       /{cr[4]}/
        EBM_A23  Slow component of mid ocean temperature               /{cr[5]}/
        EBM_A31  Fast component of deep ocean temperature              /{cr[6]}/
        EBM_A32  Intermediate component of deep ocean temperature      /{cr[7]}/
        EBM_A33  Slow component of deep ocean temperature              /{cr[8]}/
        EBM_B1   Forcing contribution to mixed layer                   /{cr[9]}/
        EBM_B2   Forcing component to ocean layer                      /{cr[10]}/
        EBM_B3   Forcing component to ocean layer                      /{cr[11]}/
        fco22x   Forcing of equilibrium CO2 doubling (Wm-2)            /{f2x}/
        nonco2(t) /1 {nonco2[0]}, 2 {nonco2[1]}, 3 {nonco2[2]}, 4 {nonco2[3]}, 5 {nonco2[4]},
                  6 {nonco2[5]}, 7 {nonco2[6]}, 8 {nonco2[7]}, 9 {nonco2[8]}, 10 {nonco2[9]},
                 11 {nonco2[10]}, 12 {nonco2[11]}, 13 {nonco2[12]}, 14 {nonco2[13]}, 15 {nonco2[14]},
                 16 {nonco2[15]}, 17 {nonco2[16]}, 18 {nonco2[17]}, 19 {nonco2[18]}, 20 {nonco2[19]},
                 21 {nonco2[20]}, 22 {nonco2[21]}, 23 {nonco2[22]}, 24 {nonco2[23]}, 25 {nonco2[24]},
                 26 {nonco2[25]}, 27 {nonco2[26]}, 28 {nonco2[27]}, 29 {nonco2[28]}, 30 {nonco2[29]},
                 31 {nonco2[30]}, 32 {nonco2[31]}, 33 {nonco2[32]}, 34 {nonco2[33]}, 35 {nonco2[34]},
                 36 {nonco2[35]}, 37 {nonco2[36]}, 38 {nonco2[37]}, 39 {nonco2[38]}, 40 {nonco2[39]},
                 41 {nonco2[40]}, 42 {nonco2[41]}, 43 {nonco2[42]}, 44 {nonco2[43]}, 45 {nonco2[44]},
                 46 {nonco2[45]}, 47 {nonco2[46]}, 48 {nonco2[47]}, 49 {nonco2[48]}, 50 {nonco2[49]},
                 51 {nonco2[50]}, 52 {nonco2[51]}, 53 {nonco2[52]}, 54 {nonco2[53]}, 55 {nonco2[54]},
                 56 {nonco2[55]}, 57 {nonco2[56]}, 58 {nonco2[57]}, 59 {nonco2[58]}, 60 {nonco2[59]},
                 61 {nonco2[60]}, 62 {nonco2[61]}, 63 {nonco2[62]}, 64 {nonco2[63]}, 65 {nonco2[64]},
                 66 {nonco2[65]}, 67 {nonco2[66]}, 68 {nonco2[67]}, 69 {nonco2[68]}, 70 {nonco2[69]},
                 71 {nonco2[70]}, 72 {nonco2[71]}, 73 {nonco2[72]}, 74 {nonco2[73]}, 75 {nonco2[74]},
                 76 {nonco2[75]}, 77 {nonco2[76]}, 78 {nonco2[77]}, 79 {nonco2[78]}, 80 {nonco2[79]},
                 81 {nonco2[80]}, 82 {nonco2[81]}, 83 {nonco2[82]}, 84 {nonco2[83]}, 85 {nonco2[84]},
                 86 {nonco2[85]}, 87 {nonco2[86]}, 88 {nonco2[87]}, 89 {nonco2[88]}, 90 {nonco2[89]},
                 91 {nonco2[90]}, 92 {nonco2[91]}, 93 {nonco2[92]}, 94 {nonco2[93]}, 95 {nonco2[94]},
                 96 {nonco2[95]}, 97 {nonco2[96]}, 98 {nonco2[97]}, 99 {nonco2[98]}, 100 {nonco2[99]},
                 101 {nonco2[100]}, 102 {nonco2[101]}, 103 {nonco2[102]}, 104 {nonco2[103]}, 105 {nonco2[104]},
                 106 {nonco2[105]}, 107 {nonco2[106]}, 108 {nonco2[107]}, 109 {nonco2[108]}, 110 {nonco2[109]},
                 111 {nonco2[110]}, 112 {nonco2[111]}, 113 {nonco2[112]}, 114 {nonco2[113]}, 115 {nonco2[114]},
                 116 {nonco2[115]}, 117 {nonco2[116]}, 118 {nonco2[117]}, 119 {nonco2[118]}, 120 {nonco2[119]},
                 121 {nonco2[120]}, 122 {nonco2[121]}, 123 {nonco2[122]}, 124 {nonco2[123]}, 125 {nonco2[124]},
                 126 {nonco2[125]}, 127 {nonco2[126]}, 128 {nonco2[127]}, 129 {nonco2[128]}, 130 {nonco2[129]},
                 131 {nonco2[130]}, 132 {nonco2[131]}, 133 {nonco2[132]}, 134 {nonco2[133]}, 135 {nonco2[134]},
                 136 {nonco2[135]}, 137 {nonco2[136]}, 138 {nonco2[137]}, 139 {nonco2[138]}, 140 {nonco2[139]},
                 141 {nonco2[140]}, 142 {nonco2[141]}, 143 {nonco2[142]}, 144 {nonco2[143]}, 145 {nonco2[144]},
                 146 {nonco2[145]}, 147 {nonco2[146]}, 148 {nonco2[147]}, 149 {nonco2[148]}, 150 {nonco2[149]},
                 151 {nonco2[150]}, 152 {nonco2[151]}, 153 {nonco2[152]}, 154 {nonco2[153]}, 155 {nonco2[154]},
                 156 {nonco2[155]}, 157 {nonco2[156]}, 158 {nonco2[157]}, 159 {nonco2[158]}, 160 {nonco2[159]}/
** Climate damage parameters:
        a2       Quadratic multiplier (Howard & Sterner 2017 base)     /0.00236/
** Abatement cost
        expcost2  Exponent of control cost function                    /2.6/
        pback     Cost of backstop 2020$ per tCO2 2023                 /679/
        gback     Initial cost decline backstop cost per period        /.025/
        limmiu    Upper limit on control rate                          /1.2/
        cprice0   Initial base carbon price (2010$ per tCO2)           /2/
        gcprice   Growth rate of base carbon price per year            /.02/

** Scaling and inessential parameters
* Note that these are unnecessary for the calculations
* They ensure that MU of first period's consumption =1 and PV cons = PV utilty
        scale1      Multiplicative scaling coefficient                 /0.0302455265681763/
        scale2      Additive scaling coefficient                       /-10993.704/ ;

* Program control variables
sets    tfirst(t), tlast(t), tearly(t), tlate(t);

PARAMETERS
        l(t)          Level of population and labor
        al(t)         Level of total factor productivity
        sigma(t)      CO2-equivalent-emissions output ratio
        rr(t)         Average utility social discount rate
        ga(t)         Growth rate of productivity from
        gl(t)         Growth rate of labor
        gcost1        Growth of cost factor
        gsig(t)       Change in sigma (cumulative improvement of energy efficiency)
        cost1(t)      Adjusted cost for backstop
        pbacktime(t)  Backstop price
        optlrsav      Optimal long-run savings rate used for transversality
        scc(t)        Social cost of carbon
        cpricebase(t) Carbon price in base case
        photel(t)     Carbon Price under no damages (Hotelling rent condition)
        ppm(t)        Atmospheric concentrations parts per million
        so2(t)        Emissions of SO2
        ch4(t)        Emissions of CH4;

* Program control definitions
        tfirst(t) = yes$(t.val eq 1);
        tlast(t)  = yes$(t.val eq card(t));
        tearly(t) = yes$(t.val<28);
        tlate(t)  = yes$(t.val>27);

* Parameters for carbon cycle
        g1 = sum(box,
                a(box) * tau(box) *
                (1 - (1 + iirf_horizon/tau(box)) * exp(-iirf_horizon/tau(box)))
             )       ;
        g0 = exp(-1 * sum(box, a(box) * tau(box) *
                (1 - exp(-iirf_horizon/tau(box))))/ g1
             );
* Further definitions of parameters
        sig0 = e0/(q0*(1-miu0));

        ga(t)=ga0*exp(-dela*tstep*((t.val-1)));
        al("1") = a0; loop(t, al(t+1)=al(t)/((1-ga(t))););
        gsig("1")=gsigma1; loop(t,gsig(t+1)=gsig(t)*((1+dsig)**tstep) ;);
        sigma("1")=sig0;   loop(t,sigma(t+1)=(sigma(t)*exp(gsig(t)*tstep)););

        pbacktime(t)=pback*(1-gback)**(t.val-1);
        cost1(t) = pbacktime(t)*sigma(t)/expcost2/1000;

        rr(t) = 1/((1+prstp)**(tstep*(t.val-1)));
        optlrsav = (dk + .004)/(dk + .004*elasmu + prstp)*gama;

* Base Case Carbon Price
        cpricebase(t)= cprice0*(1+gcprice)**(tstep*(t.val-1));

VARIABLES
        MIU(t)          Emission control rate GHGs
        FORC(t)         Increase in radiative forcing (watts per m2 from 1750)
        T1(t)           Increase temperature of atmosphere+mixed layer (degrees C from 1850-1900)
        T2(t)           Increase temperature of mid ocean (degrees C from 1850-1900)
        T3(t)           Increase temperature of deep ocean (degrees C from 1850-1900)
        co2(t)          Carbon concentration increase in atmosphere (GtC from 1750)
        E(t)            Total CO2 emissions (GtCO2 per year)
        EIND(t)         Industrial emissions (GtCO2 per year)
        C(t)            Consumption (trillions 2005 US dollars per year)
        K(t)            Capital stock (trillions 2005 US dollars)
        CPC(t)          Per capita consumption (thousands 2005 USD per year)
        I(t)            Investment (trillions 2005 USD per year)
        S(t)            Gross savings rate as fraction of gross world product
        RI(t)           Real interest rate (per annum)
        Y(t)            Gross world product net of abatement and damages (trillions 2005 USD per year)
        YGROSS(t)       Gross world product GROSS of abatement and damages (trillions 2005 USD per year)
        YNET(t)         Output net of damages equation (trillions 2005 USD per year)
        DAMAGES(t)      Damages (trillions 2005 USD per year)
        DAMFRAC(t)      Damages as fraction of gross output
        ABATECOST(t)    Cost of emissions reductions  (trillions 2005 USD per year)
        MCABATE(t)      Marginal cost of abatement (2005$ per ton CO2)
        CCA(t)          Cumulative industrial carbon emissions (GtC)
        CCATOT(t)       Total carbon emissions (GtC)
        PERIODU(t)      One period utility function
        CPRICE(t)       Carbon price (2005$ per ton of CO2)
        CEMUTOTPER(t)   Period utility
        UTILITY         Welfare function
        cbox1(t)        Carbon in box 1
        cbox2(t)        Carbon in box 2
        cbox3(t)        Carbon in box 3
        cbox4(t)        Carbon in box 4
        alpha(t)        Time-varying scale factor for CO2 carbon box timescale
        iirf(t)         time-integrated impulse response
        atfrac(t)       Atmospheric share since 1850
        etree(t)        Land use emissions
        cumetree(t)     Cumulative land use emissions;

NONNEGATIVE VARIABLES  MIU, T1, co2, MU, ML, Y, YGROSS, C, K, I, alpha, cprice;

EQUATIONS
*Emissions and Damages
        EEQ(t)          Emissions equation
        EINDEQ(t)       Industrial emissions
        CCAEQ(t)       Cumulative industrial carbon emissions
        CCATOTEQ(t)     Cumulative total carbon emissions
        FORCEQ(t)        Radiative forcing equation
        DAMFRACEQ(t)    Equation for damage fraction
        DAMEQ(t)        Damage equation
        ABATEEQ(t)      Cost of emissions reductions equation
        MCABATEEQ(t)    Equation for MC abatement
        CARBPRICEEQ(t)  Carbon price equation from abatement

*Climate and carbon cycle
        co2eq(t)         Atmospheric concentration equation
        ATFRACEQ(t)      Atmospheric airborne fraction equation
        T1EQ(t)          Temperature-climate equation for atmosphere + mixed layer
        T2EQ(t)          Temperature-climate equation for mid ocean
        T3EQ(t)          Temperature-climate equation for deep ocean
        ALPHAEQ(t)       Scale factor equation
        IIRFEQ(t)        IIRF equation
        CBOX1EQ(t)       Carbon box 1 equation
        CBOX2EQ(t)       Carbon box 2 equation
        CBOX3EQ(t)       Carbon box 3 equation
        CBOX4EQ(t)       Carbon box 4 equation
        etreeeq(t)       land use eq
        cumetreeeq(t)    cumulative land use eq
*        nonco2eq1(t)     non-CO2 forcing eq
*        nonco2eq2(t)     non-CO2 forcing eq
*constrainT  if we want to e.g. limit warming to 2 degrees

*Economic variables
        YGROSSEQ(t)      Output gross equation
        YNETEQ(t)        Output net of damages equation
        YY(t)            Output net equation
        CC(t)            Consumption equation
        CPCE(t)          Per capita consumption definition
        SEQ(t)           Savings rate equation
        KK(t)            Capital balance equation
        RIEQ(t)          Interest rate equation

* Utility
        CEMUTOTPEREQ(t)  Period utility
        PERIODUEQ(t)     Instantaneous utility function equation
        UTIL             Objective function;

** Equations of the model
* Emissions and Damages
 eeq(t)..             E(t)           =E= EIND(t) + etree(t);
 eindeq(t)..          EIND(t)        =E= sigma(t) * YGROSS(t) * (1-(MIU(t)));
 ccaeq(t+1)..         CCA(t+1)       =E= CCA(t)+ EIND(t)*tstep/3.664;
 ccatoteq(t)..        CCATOT(t)      =E= CCA(t)+cumetree(t);
* nonco2eq1(tearly)..  nonco2(tearly) =E= {nonco2_const} + ({nonco2_ffi})*EIND(tearly) + ({nonco2_quantile})*quantile + ({nonco2_period})*tearly.val;
* nonco2eq2(tlate)..   nonco2(tlate)  =E= {nonco2_const} + ({nonco2_ffi})*EIND(tlate) + ({nonco2_quantile})*quantile + ({nonco2_period})*27;
 forceq(t)..          FORC(t)        =E= fco22x * ((log((CO2(t)/co2_1750))/log(2))) + nonco2(t);
 damfraceq(t) ..      DAMFRAC(t)     =E= a2*T1(t)**2;
 dameq(t)..           DAMAGES(t)     =E= YGROSS(t) * DAMFRAC(t);
 abateeq(t)..         ABATECOST(t)   =E= YGROSS(t) * cost1(t) * (MIU(t)**expcost2);
 mcabateeq(t)..       MCABATE(t)     =E= pbacktime(t) * MIU(t)**(expcost2-1);
 carbpriceeq(t)..     CPRICE(t)      =E= pbacktime(t) * (MIU(t))**(expcost2-1);
 etreeeq(t)..         etree(t)       =e= ({afolu_const} + ({afolu_ffi})*EIND(t) + ({afolu_period})*t.val) * (1 - 1/(1+exp(-1.00*(t.val-35))));
 cumetreeeq(t+1)..    cumetree(t+1)  =e= cumetree(t) + etree(t)*tstep/3.664;

* Climate and carbon cycle
 atfraceq(t)..        atfrac(t)      =E= ((co2(t)-co2_1750)/(ccatot(t)+0.0000001));
 iirfeq(t)..          IIRF(t)        =E= r0 + ru * (1-atfrac(t)) * ccatot(t)*3.664 + rt * T1(t) + ra * atfrac(t) * ccatot(t)*3.664;
 alphaeq(t)..         ALPHA(t)       =E= g0 * exp(iirf(t)/g1);
 cbox1eq(t+1)..       CBOX1(t+1)     =E= a("1")*E(t)/3.664 * alpha(t)*tau("1") * (1 - exp(-tstep/(alpha(t)*tau("1"))))  + cbox1(t) * exp(-tstep/(alpha(t)*tau("1")));
 cbox2eq(t+1)..       CBOX2(t+1)     =E= a("2")*E(t)/3.664 * alpha(t)*tau("2") * (1 - exp(-tstep/(alpha(t)*tau("2"))))  + cbox2(t) * exp(-tstep/(alpha(t)*tau("2")));
 cbox3eq(t+1)..       CBOX3(t+1)     =E= a("3")*E(t)/3.664 * alpha(t)*tau("3") * (1 - exp(-tstep/(alpha(t)*tau("3"))))  + cbox3(t) * exp(-tstep/(alpha(t)*tau("3")));
 cbox4eq(t+1)..       CBOX4(t+1)     =E= a("4")*E(t)/3.664 * alpha(t)*tau("4") * (1 - exp(-tstep/(alpha(t)*tau("4"))))  + cbox4(t) * exp(-tstep/(alpha(t)*tau("4")));
 T1eq(t+1)..          T1(t+1)        =E= EBM_A11 * T1(t) + EBM_A12 * T2(t) + EBM_A13 * T3(t) + EBM_B1 * FORC(t);
 t2eq(t+1)..          T2(t+1)        =E= EBM_A21 * T1(t) + EBM_A22 * T2(t) + EBM_A23 * T3(t) + EBM_B2 * FORC(t);
 t3eq(t+1)..          T3(t+1)        =E= EBM_A31 * T1(t) + EBM_A32 * T2(t) + EBM_A33 * T3(t) + EBM_B3 * FORC(t);
 co2eq(t)..           co2(t)         =E= co2_1750 + cbox1(t) + cbox2(t) + cbox3(t) + cbox4(t);
* constrainT(t)..     T1(t)          =L= 2;

* Economic variables
 ygrosseq(t)..        YGROSS(t)      =E= (al(t)*(L(t))**(1-GAMA))*(K(t)**GAMA);
 yneteq(t)..          YNET(t)        =E= YGROSS(t)*(1-damfrac(t));
 yy(t)..              Y(t)           =E= YNET(t) - ABATECOST(t);
 cc(t)..              C(t)           =E= Y(t) - I(t);
 cpce(t)..            CPC(t)         =E= C(t) / L(t);
 seq(t)..             I(t)           =E= S(t) * Y(t);
 kk(t+1)..            K(t+1)         =L= (1-dk)**tstep * K(t) + tstep * I(t);
 rieq(t+1)..          RI(t)          =E= (1+prstp) * (CPC(t+1)/CPC(t))**(elasmu/tstep) - 1;

* Utility
 cemutotpereq(t)..    CEMUTOTPER(t)  =E= PERIODU(t) * L(t)*1000 * rr(t);
 periodueq(t)..       PERIODU(t)     =E= ((C(T)/L(T))**(1-elasmu)-1)/(1-elasmu)-1;
 util..               UTILITY        =E= tstep * scale1 * sum(t,  CEMUTOTPER(t)) + scale2 ;

* Resource limit
CCA.up(t)             = fosslim;
CCA.lo(t)             = 0;

* Control rate limits
MIU.up(t)             = limmiu;
MIU.up(t)$(t.val<8)   = 0.15*t.val;
*MIU.up(t)$(t.val<10)  = 1;

** Upper and lower bounds for stability
K.LO(t)         = 1;
EIND.LO(t)      = -50;
co2.LO(t)       = 10;
MU.LO(t)        = 100;
ML.LO(t)        = 1000;
C.LO(t)         = 2;
T2.UP(t)        = 15;
T2.LO(t)        = -1;
T3.UP(t)        = 10;
T3.LO(t)        = -1;
T1.UP(t)        = 20;
CPC.LO(t)       = .01;
T1.UP(t)        = 12;
IIRF.UP(t)      = 97;
IIRF.LO(t)      = 16;
alpha.lo(t)     = 0.01;
alpha.up(t)     = 100;

* Control variables
set lag10(t) ;
lag10(t) =  yes$(t.val gt card(t)-10);
S.FX(lag10(t)) = optlrsav;

* Initial conditions
CCA.FX(tfirst)    = 478.6667;
K.FX(tfirst)      = k0;
co2.FX(tfirst)     = co2_2023;
T1.FX(tfirst)   = T1_0;
T2.FX(tfirst)   = T2_0;
T3.FX(tfirst)   = T3_0;
IIRF.l(tfirst)    = 50;
atfrac.l(tfirst)  = 0.526;
alpha.l(tfirst)   = 0.81;
*these three lines above need a check
cbox1.fx(tfirst)  = icbox1;
cbox2.fx(tfirst)  = icbox2;
cbox3.fx(tfirst)  = icbox3;
cbox4.fx(tfirst)  = icbox4;
cumetree.fx(tfirst) = 233.7448;

** Solution options
option iterlim = 99999;
option reslim  = 99999;
option solprint = on;
option limrow = 0;
option limcol = 0;
model  DICE /all/;

miu.fx('1')$(ifopt=1) = miu0;
solve DICE maximizing utility using nlp;
solve DICE maximizing utility using nlp;
solve DICE maximizing utility using nlp;

** POST-SOLVE
* Calculate social cost of carbon and other variables
scc(t)        = -1000*eeq.m(t)/(.00001+cc.m(t));
ppm(t)        = co2.l(t)/{carbon_convert};

** CALCULATE NON-CO2 EMISSIONS
so2(tearly) = 65.8889 + 0.4514*eind.l(tearly) - 5.3944*tearly.val + 0.1335*tearly.val**2;
so2(tlate)  = 65.8889 + 0.4514*eind.l(tlate) - 5.3944*27 + 0.1335*27**2;
ch4(tearly) = 203.4439 + 4.2581*eind.l(tearly) - 5.2576*tearly.val + 0.1471*tearly.val**2;
ch4(tlate)  = 203.4439 + 4.2581*eind.l(tlate) - 5.2576*27 + 0.1471*27**2;

* Produces a file "Dice2016R-091916ap.csv" in the base directory
* For ALL relevant model outputs, see 'PutOutputAllT.gms' in the Include folder.
* The statement at the end of the *.lst file "Output..." will tell you where to find the file.

file results /"{here}/../data_output/dice_below2deg/{config:07d}.csv"/; results.nd = 10 ; results.nw = 0 ; results.pw=20000; results.pc=5;
put results;
put // "Period";
Loop (T, put T.val);
put / "Year" ;
Loop (T, put (2020+(TSTEP*T.val) ));
put / "Industrial Emissions GTCO2 per year" ;
Loop (T, put EIND.l(T));
put / "Atmospheric concentrations ppm" ;
Loop (T, put ppm(t));
put / "Atmospheric Temperature rel. 1850-1900" ;
Loop (T, put T1.l(T));
put / "Mid-ocean Temperature rel. 1850-1900" ;
Loop (T, put T2.l(T));
put / "Deep-ocean temperature rel. 1850-1900" ;
Loop (T, put T3.l(T));
put / "Output Net Net " ;
Loop (T, put Y.l(T));
put / "Climate Damages fraction output" ;
Loop (T, put DAMFRAC.l(T));
put / "Consumption Per Capita " ;
Loop (T, put CPC.l(T));
put / "Carbon Price (per t CO2)" ;
Loop (T, put cprice.l(T));
put / "Emissions Control Rate" ;
Loop (T, put MIU.l(T));
put / "Social cost of carbon" ;
Loop (T, put scc(T));
put / "Interest Rate " ;
Loop (T, put RI.l(T));
put / "Population" ;
Loop (T, put L(T));
put / "TFP" ;
Loop (T, put AL(T));
put / "Output gross,gross" ;
Loop (T, put YGROSS.L(t));
put / "Change tfp" ;
Loop (T, put ga(t));
put / "Capital" ;
Loop (T, put k.l(t));
put / "s" ;
Loop (T, put s.l(t));
put / "I" ;
Loop (T, put I.l(t));
put / "Y gross net" ;
Loop (T, put ynet.l(t));
put / "damages" ;
Loop (T, put damages.l(t));
put / "damfrac" ;
Loop (T, put damfrac.l(t));
put / "abatement" ;
Loop (T, put abatecost.l(t));
put / "sigma" ;
Loop (T, put sigma(t));
put / "Forcings" ;
Loop (T, put forc.l(t));
put / "Other Forcings" ;
Loop (T, put nonco2(t));
put / "Period utilty" ;
Loop (T, put periodu.l(t));
put / "Consumption" ;
Loop (T, put C.l(t));
put / "Land emissions" ;
Loop (T, put etree.l(t));
put / "Cumulative ind emissions" ;
Loop (T, put cca.l(t));
put / "Cumulative total emissions" ;
Loop (T, put ccatot.l(t));
put / "Atmospheric concentrations Gt" ;
Loop (T, put co2.l(t));
put / "Total Emissions GTCO2 per year" ;
Loop (T, put E.l(T));
put / "Airborne fraction since 1750" ;
Loop (T, put atfrac.l(t));
put / "alpha" ;
Loop (T, put alpha.l(t));
put / "IIRF" ;
Loop (T, put iirf.l(t));
put / "cbox1" ;
Loop (T, put cbox1.l(t));
put / "cbox2" ;
Loop (T, put cbox2.l(t));
put / "cbox3" ;
Loop (T, put cbox3.l(t));
put / "cbox4" ;
Loop (T, put cbox4.l(t));
put / "so2" ;
Loop (T, put so2(t));
put / "ch4" ;
Loop (T, put ch4(t));
put / "Objective" ;
put utility.l;
putclose;
    '''

    # write the script
    with open(os.path.join(here, 'gams_scripts', f'config{config:07d}.gms'), 'w') as f:
        f.write(template)

    # run the command
    with open(os.path.join(here, 'gams_scripts', f'config{config:07d}.out'), "w") as outfile:
        subprocess.run(
            [
                'gams',
                os.path.join(
                    here,
                    'gams_scripts',
                    f'config{config:07d}.gms'
                ),
                '-o',
                os.path.join(
                    here,
                    'gams_scripts',
                    f'config{config:07d}.lst'
                ),
            ],
            stdout = outfile,
        )


    # were results feasible?
    with open(os.path.join(here, 'gams_scripts', f'config{config:07d}.lst')) as f:
        output = f.read()
        if " ** Infeasible solution. Reduced gradient less than tolerance." in output:
            raise InfeasibleSolutionError(run)
