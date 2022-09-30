# TODO: change cumulative emissions to SSP119

import json
import os
import subprocess

from tqdm import tqdm
import pandas as pd

# should really import these constants from FaIR
carbon_convert = 5.1352 * 12.011 / 28.97

here = os.path.dirname(os.path.realpath(__file__))

df_configs = pd.read_csv(os.path.join(here, '..', 'data_input', 'fair-2.1.0', 'ar6_calibration_ebm3.csv'), index_col=0)
configs = df_configs.index

os.makedirs(os.path.join(here, 'gams_scripts'), exist_ok=True)
os.makedirs(os.path.join(here, '..', 'data_output', 'dice_1p5deglowOS'), exist_ok=True)

df_nonco2 = pd.read_csv(os.path.join(here, '..', 'data_output', 'climate_configs', 'anthropogenic_non-co2_forcing_ssp119.csv'), index_col=0)
df_cbox = pd.read_csv(os.path.join(here, '..', 'data_output', 'climate_configs', 'gas_partitions_ssp119.csv'), index_col=0)
df_cr = pd.read_csv(os.path.join(here, '..', 'data_output', 'climate_configs', 'climate_response_params.csv'), index_col=0)
df_co2 = pd.read_csv(os.path.join(here, '..', 'data_output', 'climate_configs', 'co2_forcing_ssp119.csv'), index_col=0)
df_temp = pd.read_csv(os.path.join(here, '..', 'data_output', 'climate_configs', 'temperature_ssp119.csv'), index_col=0)

df_pop = pd.read_csv(os.path.join(here, '..', 'data_input', 'un-population', 'un-median-projections-20220928.csv'), index_col=0)
pop = df_pop['population_bn'].values

infeas = 0
n_configs = 1001

for run, config in tqdm(enumerate(configs[:n_configs])):
    t1 = df_temp.loc[config, 'mixed_layer']
    t2 = df_temp.loc[config, 'mid_ocean']
    t3 = df_temp.loc[config, 'deep_ocean']
    nonco2 = df_nonco2.loc[config, :].values
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
    co2_2020 = df_cbox.loc[config, 'co2_2020']
    co2_1750 = df_configs.loc[config, 'co2_concentration_1750']

    template = f'''
$ontext
DICE with FaIR carbon cycle and climate response.

Climate module by Chris Smith, 28 June 2022. Economic model is unmodified from the
beta version of DICE-2016R, by William Nordhaus, and downloaded from
http://www.econ.yale.edu/~nordhaus/homepage/homepage/DICE2016R-091916ap.gms

Version is DICE-2016R-091916ap.gms
$offtext

$title        DICE-2016R-FAIR June 2022

set     t        Time periods (5 years per period)                     /1*100/
        box      Carbon box                                            /1*4/

PARAMETERS
** Availability of fossil fuels
        fosslim  Maximum cumulative extraction fossil fuels (GtC)      /6000/
**Time Step
        tstep    Years per Period                                      /5/
** If optimal control
        ifopt    Indicator where optimized is 1 and base is 0          /1/
** Preferences
        elasmu   Elasticity of marginal utility of consumption         /1.45/
        prstp    Initial rate of social time preference per year       /0.015/
** Technology and population (updated by CS)
        gama     Capital elasticity in production function             /0.300/
        dk       Depreciation rate on capital (per year)               /0.100/
        q0       Initial world gross output 2020 (trill 2020 USD)      /133.7/
        k0       Initial capital value 2019                            /318.7/
        a0       Initial level of total factor productivity            /5.611213/
        ga0      Initial growth rate for TFP per 5 years               /0.076/
        dela     Decline rate of TFP per 5 years                       /0.005/
        l(t)     /1 {pop[0]}, 2 {pop[1]}, 3 {pop[2]}, 4 {pop[3]}, 5 {pop[4]},
                  6 {pop[5]}, 7 {pop[6]}, 8 {pop[7]}, 9 {pop[8]}, 10 {pop[9]},
                 11 {pop[10]}, 12 {pop[11]}, 13 {pop[12]}, 14 {pop[13]}, 15 {pop[14]},
                 16 {pop[15]}, 17 {pop[16]}, 18 {pop[16]}, 19 {pop[16]}, 20 {pop[16]},
                 21 {pop[16]}, 22 {pop[16]}, 23 {pop[16]}, 24 {pop[16]}, 25 {pop[16]},
                 26 {pop[16]}, 27 {pop[16]}, 28 {pop[16]}, 29 {pop[16]}, 30 {pop[16]},
                 31 {pop[16]}, 32 {pop[16]}, 33 {pop[16]}, 34 {pop[16]}, 35 {pop[16]},
                 36 {pop[16]}, 37 {pop[16]}, 38 {pop[16]}, 39 {pop[16]}, 40 {pop[16]},
                 41 {pop[16]}, 42 {pop[16]}, 43 {pop[16]}, 44 {pop[16]}, 45 {pop[16]},
                 46 {pop[16]}, 47 {pop[16]}, 48 {pop[16]}, 49 {pop[16]}, 50 {pop[16]},
                 51 {pop[16]}, 52 {pop[16]}, 53 {pop[16]}, 54 {pop[16]}, 55 {pop[16]},
                 56 {pop[16]}, 57 {pop[16]}, 58 {pop[16]}, 59 {pop[16]}, 60 {pop[16]},
                 61 {pop[16]}, 62 {pop[16]}, 63 {pop[16]}, 64 {pop[16]}, 65 {pop[16]},
                 66 {pop[16]}, 67 {pop[16]}, 68 {pop[16]}, 69 {pop[16]}, 70 {pop[16]},
                 71 {pop[16]}, 72 {pop[16]}, 73 {pop[16]}, 74 {pop[16]}, 75 {pop[16]},
                 76 {pop[16]}, 77 {pop[16]}, 78 {pop[16]}, 79 {pop[16]}, 80 {pop[16]},
                 81 {pop[16]}, 82 {pop[16]}, 83 {pop[16]}, 84 {pop[16]}, 85 {pop[16]},
                 86 {pop[16]}, 87 {pop[16]}, 88 {pop[16]}, 89 {pop[16]}, 90 {pop[16]},
                 91 {pop[16]}, 92 {pop[16]}, 93 {pop[16]}, 94 {pop[16]}, 95 {pop[16]},
                 96 {pop[16]}, 97 {pop[16]}, 98 {pop[16]}, 99 {pop[16]}, 100 {pop[16]}/
** Emissions parameters
        gsigma1  Initial growth of sigma (per year)                    /-0.0152/
        dsig     Decline rate of decarbonization (per period)          /-0.001/
        eland0   Carbon emissions from land 2020 (GtCO2 per year)      /3.26/
* projections from RCMIP (should use GCP; TODO)
        deland   Decline rate of land emissions (per period)           /0.115/
        e0       Industrial emissions 2020 (GtCO2 per year)            /37.39/
* projections from RCMIP (should use GCP; TODO)
        miu0     Initial emissions control rate for base case 2020     /0.15/
* Initial Conditions
        co2_2020 Initial concentration in atmosphere 2020 (GtC)        /{co2_2020*carbon_convert}/
        co2_1750 Pre-industrial concentration atmosphere  (GtC)        /{co2_1750*carbon_convert}/
* These are for declaration and are defined later
        sig0     Carbon intensity 2010 (kgCO2 per output 2005 USD 2010)
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
        ICBOX1   Initial GtC concentration of carbon box 1 in 2020     /{cbox1}/
        ICBOX2   Initial GtC concentration of carbon box 2 in 2020     /{cbox2}/
        ICBOX3   Initial GtC concentration of carbon box 3 in 2020     /{cbox3}/
        ICBOX4   Initial GtC concentration of carbon box 4 in 2020     /{cbox4}/
        forcoth(t) /1 {nonco2[0]}, 2 {nonco2[1]}, 3 {nonco2[2]}, 4 {nonco2[3]}, 5 {nonco2[4]},
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
                  96 {nonco2[95]}, 97 {nonco2[96]}, 98 {nonco2[96]}, 99 {nonco2[96]}, 100 {nonco2[96]}/
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
** Climate damage parameters
        a10      Initial damage intercept                              /0/
        a20      Initial damage quadratic term
        a1       Damage intercept                                      /0/
        a2       Damage quadratic term                                 /0.00236/
        a3       Damage exponent                                       /2.00/
** Abatement cost
        expcost2  Exponent of control cost function                    /2.6/
        pback     Cost of backstop 2020$ per tCO2 2020                 /679/
        gback     Initial cost decline backstop cost per period        /.025/
        limmiu    Upper limit on control rate after 2150               /1.2/
        tnopol    Period before which no emissions controls base       /45/
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
        forcoth(t)    Exogenous forcing for other greenhouse gases
        gl(t)         Growth rate of labor
        gcost1        Growth of cost factor
        gsig(t)       Change in sigma (cumulative improvement of energy efficiency)
        etree(t)      Emissions from deforestation
        cumetree(t)   Cumulative from land
        cost1(t)      Adjusted cost for backstop
        pbacktime(t)  Backstop price
        optlrsav      Optimal long-run savings rate used for transversality
        scc(t)        Social cost of carbon
        cpricebase(t) Carbon price in base case
        photel(t)     Carbon Price under no damages (Hotelling rent condition)
        ppm(t)        Atmospheric concentrations parts per million;

* Program control definitions
        tfirst(t) = yes$(t.val eq 1);
        tlast(t)  = yes$(t.val eq card(t));
        tearly(t) = yes$(t.val le 16);
        tlate(t)  = yes$(t.val gt 16);
        alias(tearly, tearly_dummy);

* Parameters for carbon cycle
        g1 = sum(box,
                a(box) * tau(box) *
                (1 - (1 + iirf_horizon/tau(box)) * exp(-iirf_horizon/tau(box)))
             )       ;
        g0 = exp(-1 * sum(box, a(box) * tau(box) *
                (1 - exp(-iirf_horizon/tau(box))))/ g1
             );
* Further definitions of parameters
        a20 = a2;
        sig0 = e0/(q0*(1-miu0));

        ga(t)=ga0*exp(-dela*5*((t.val-1)));
        al("1") = a0; loop(t, al(t+1)=al(t)/((1-ga(t))););
        gsig("1")=gsigma1; loop(t,gsig(t+1)=gsig(t)*((1+dsig)**tstep) ;);
        sigma("1")=sig0;   loop(t,sigma(t+1)=(sigma(t)*exp(gsig(t)*tstep)););

        pbacktime(t)=pback*(1-gback)**(t.val-1);
        cost1(t) = pbacktime(t)*sigma(t)/expcost2/1000;

        etree(t) = eland0*(1-deland)**(t.val-1);
        cumetree("1")= 190.9; loop(t,cumetree(t+1)=cumetree(t)+etree(t)*(5/3.664););

        rr(t) = 1/((1+prstp)**(tstep*(t.val-1)));
        optlrsav = (dk + .004)/(dk + .004*elasmu + prstp)*gama;

* Base Case Carbon Price
        cpricebase(t)= cprice0*(1+gcprice)**(5*(t.val-1));

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
        atfrac(t)       Atmospheric share since 1850;

NONNEGATIVE VARIABLES  MIU, T1, co2, MU, ML, Y, YGROSS, C, K, I, alpha;

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
        constrainTlong   limit long-term warming to 1.5 degrees

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
 forceq(t)..          FORC(t)        =E= fco22x * ((log((CO2(t)/co2_1750))/log(2))) + forcoth(t);
 damfraceq(t) ..      DAMFRAC(t)     =E= (a1*T1(t))+(a2*T1(t)**a3) ;
 dameq(t)..           DAMAGES(t)     =E= YGROSS(t) * DAMFRAC(t);
 abateeq(t)..         ABATECOST(t)   =E= YGROSS(t) * cost1(t) * (MIU(t)**expcost2);
 mcabateeq(t)..       MCABATE(t)     =E= pbacktime(t) * MIU(t)**(expcost2-1);
 carbpriceeq(t)..     CPRICE(t)      =E= pbacktime(t) * (MIU(t))**(expcost2-1);

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
 constrainTlong(t)..  T1(t)          =L= 1.5;

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
MIU.up(t)$(t.val<8)  = 1;

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
CCA.FX(tfirst)    = 470.55;
K.FX(tfirst)      = k0;
co2.FX(tfirst)     = co2_2020;
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

** Solution options
option iterlim = 99999;
option reslim  = 99999;
option solprint = on;
option limrow = 0;
option limcol = 0;
model  DICE /all/;

* For base run, this subroutine calculates Hotelling rents
* Carbon price is maximum of Hotelling rent or baseline price
* The cprice equation is different from 2013R. Not sure what went wrong.
If (ifopt eq 0,
       a2 = 0;
       solve DICE maximizing UTILITY using nlp;
       photel(t)=cprice.l(t);
       a2 = a20;
      cprice.up(t)$(t.val<tnopol+1) = max(photel(t),cpricebase(t));
);

miu.fx('1')$(ifopt=1) = miu0;
solve DICE maximizing utility using nlp;
solve DICE maximizing utility using nlp;
solve DICE maximizing utility using nlp;

** POST-SOLVE
* Calculate social cost of carbon and other variables
scc(t)        = -1000*eeq.m(t)/(.00001+cc.m(t));
ppm(t)        = co2.l(t)/{carbon_convert};

* Produces a file "Dice2016R-091916ap.csv" in the base directory
* For ALL relevant model outputs, see 'PutOutputAllT.gms' in the Include folder.
* The statement at the end of the *.lst file "Output..." will tell you where to find the file.

file results /"{here}/../data_output/dice_1p5deglowOS/{config:07d}.csv"/; results.nd = 10 ; results.nw = 0 ; results.pw=20000; results.pc=5;
put results;
put // "Period";
Loop (T, put T.val);
put / "Year" ;
Loop (T, put (2015+(TSTEP*T.val) ));
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
Loop (T, put forcoth(t));
put / "Period utilty" ;
Loop (T, put periodu.l(t));
put / "Consumption" ;
Loop (T, put C.l(t));
put / "Land emissions" ;
Loop (T, put etree(t));
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
        fail_1 = " ** Infeasible solution. Reduced gradient less than tolerance." in output
        last_infeasible_mention = output.rfind("INFEASIBLE")
        n_infeasible = int(output[last_infeasible_mention-10:last_infeasible_mention])
        fail_2 = n_infeasible > 0
#        fail_3 = " ** Infeasible solution. The solution process has been terminated" in output
        if fail_1 or fail_2:
            # tally number of infeasibilities
            infeas = infeas + 1

            # Sometimes CSV output is produced and is nonsense, sometimes it isn't produced.
            # If it isn't, trying to delete a non-existing file will cause an error, so
            # check first
            if os.path.isfile(os.path.join(here, '..', 'data_output', 'dice_1p5deglowOS', f'{config:07d}.csv')):
                os.remove(os.path.join(here, '..', 'data_output', 'dice_1p5deglowOS', f'{config:07d}.csv'))

print(f'{infeas} out of {n_configs} were infeasible')
