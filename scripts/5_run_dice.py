import json
import os
import subprocess

from tqdm import tqdm
import pandas as pd
from climateforcing.utils import mkdir_p
import fair

class InfeasibleSolutionError(Exception):
    def __init__(self, run):
        print(f"Infeasible solution in run number {run}.")

here = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(here, '..', 'data_input', 'fair-1.6.2', 'fair-1.6.2-wg3-params.json')) as f:
    config_list = json.load(f)
ensemble_size=len(config_list)

mkdir_p(os.path.join(here, 'gams_scripts'))
mkdir_p(os.path.join(here, '..', 'data_output', 'dice'))

# TODO: rename output CSVs and different index column
df_t2 = pd.read_csv(os.path.join(here, '..', 'data_input', 'wg1', 'temperature_ocean_2015.csv'))
df_nonco2 = pd.read_csv(os.path.join(here, '..', 'data_output', 'anthropogenic-non-co2-forcing.csv'), index_col=0)
df_cbox = pd.read_csv(os.path.join(here, '..', 'data_output', 'carbon-boxes.csv'), index_col=0)
df_cr = pd.read_csv(os.path.join(here, '..', 'data_output', 'climate_response_params.csv'), index_col=0)
df_cc = pd.read_csv(os.path.join(here, '..', 'data_output', 'cc-feedbacks.csv'), index_col=0)
df_t1 = pd.read_csv(os.path.join(here, '..', 'data_output', 'temperature.csv'), index_col=0)

for run in tqdm(range(ensemble_size)):
    t2 = df_t2.loc[run].values[0]
    foth = df_nonco2.iloc[:,run].values
    cbox = df_cbox.loc[run].values
    cr = df_cr.loc[run].values
    cc = df_cc.loc[run].values
    t1 = df_t1.loc[run].values[0]

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
** Population and technology
        gama     Capital elasticity in production function             /0.300/
        pop0     Initial world population 2015 (millions)              /7403/
        popadj   Growth rate to calibrate to 2050 pop projection       /0.134/
        popasym  Asymptotic population (millions)                      /11500/
        dk       Depreciation rate on capital (per year)               /0.100/
        q0       Initial world gross output 2015 (trill 2010 USD)      /105.5/
        k0       Initial capital value 2015 (trill 2010 USD)           /223/
        a0       Initial level of total factor productivity            /5.115/
        ga0      Initial growth rate for TFP per 5 years               /0.076/
        dela     Decline rate of TFP per 5 years                       /0.005/
** Emissions parameters
        gsigma1  Initial growth of sigma (per year)                    /-0.0152/
        dsig     Decline rate of decarbonization (per period)          /-0.001/
        eland0   Carbon emissions from land 2015 (GtCO2 per year)      /4.14/
* Global Carbon Project 2021, average of 2010-2020 LUC emissions
        deland   Decline rate of land emissions (per period)           /0.115/
        e0       Industrial emissions 2015 (GtCO2 per year)            /35.85/
        miu0     Initial emissions control rate for base case 2015     /0.03/
* Initial Conditions
        mat0     Initial Concentration in atmosphere 2015 (GtC)        /{cc[3]*fair.constants.general.ppm_gtc+cbox.sum()}/
        mateq    Equilibrium concentration atmosphere  (GtC)           /{cc[3]*fair.constants.general.ppm_gtc}/
* These are for declaration and are defined later
        sig0     Carbon intensity 2010 (kgCO2 per output 2005 USD 2010)
** Climate model parameters
        g0       Carbon cycle parameter (Leach et al. 2021)
        g1       Carbon cycle parameter (Leach et al. 2021)
        r0       Pre-industrial time-integrated airborne fraction      /{cc[0]}/
        rc       Sensitivity of airborne fraction with cumulative CO2  /{cc[1]}/
        rt       Sensitivity of airborne fraction with temperature     /{cc[2]}/
        tau(box) Lifetimes of the four atmospheric carbon boxes
                     / 1 1e9, 2 394.4, 3 36.54, 4 4.304 /
        a(box)   Partition fraction of the four atmospheric carbon boxes
                     / 1 0.2173, 2 0.2240, 3 0.2824, 4 0.2763 /
        ICBOX1   Initial GtC concentration of carbon box 1 in 2015     /{cbox[0]}/
        ICBOX2   Initial GtC concentration of carbon box 2 in 2015     /{cbox[1]}/
        ICBOX3   Initial GtC concentration of carbon box 3 in 2015     /{cbox[2]}/
        ICBOX4   Initial GtC concentration of carbon box 4 in 2015     /{cbox[3]}/
        forcoth(t) /1 {foth[0]}, 2 {foth[1]}, 3 {foth[2]}, 4 {foth[3]}, 5 {foth[4]},
                  6 {foth[5]}, 7 {foth[6]}, 8 {foth[7]}, 9 {foth[8]}, 10 {foth[9]},
                  11 {foth[10]}, 12 {foth[11]}, 13 {foth[12]}, 14 {foth[13]}, 15 {foth[14]},
                  16 {foth[15]}, 17 {foth[16]}, 18 {foth[17]}, 19 {foth[18]}, 20 {foth[19]},
                  21 {foth[20]}, 22 {foth[21]}, 23 {foth[22]}, 24 {foth[23]}, 25 {foth[24]},
                  26 {foth[25]}, 27 {foth[26]}, 28 {foth[27]}, 29 {foth[28]}, 30 {foth[29]},
                  31 {foth[30]}, 32 {foth[31]}, 33 {foth[32]}, 34 {foth[33]}, 35 {foth[34]},
                  36 {foth[35]}, 37 {foth[36]}, 38 {foth[37]}, 39 {foth[38]}, 40 {foth[39]},
                  41 {foth[40]}, 42 {foth[41]}, 43 {foth[42]}, 44 {foth[43]}, 45 {foth[44]},
                  46 {foth[45]}, 47 {foth[46]}, 48 {foth[47]}, 49 {foth[48]}, 50 {foth[49]},
                  51 {foth[50]}, 52 {foth[51]}, 53 {foth[52]}, 54 {foth[53]}, 55 {foth[54]},
                  56 {foth[55]}, 57 {foth[56]}, 58 {foth[57]}, 59 {foth[58]}, 60 {foth[59]},
                  61 {foth[60]}, 62 {foth[61]}, 63 {foth[62]}, 64 {foth[63]}, 65 {foth[64]},
                  66 {foth[65]}, 67 {foth[66]}, 68 {foth[67]}, 69 {foth[68]}, 70 {foth[69]},
                  71 {foth[70]}, 72 {foth[71]}, 73 {foth[72]}, 74 {foth[73]}, 75 {foth[74]},
                  76 {foth[75]}, 77 {foth[76]}, 78 {foth[77]}, 79 {foth[78]}, 80 {foth[79]},
                  81 {foth[80]}, 82 {foth[81]}, 83 {foth[82]}, 84 {foth[83]}, 85 {foth[84]},
                  86 {foth[85]}, 87 {foth[86]}, 88 {foth[87]}, 89 {foth[88]}, 90 {foth[89]},
                  91 {foth[90]}, 92 {foth[91]}, 93 {foth[92]}, 94 {foth[93]}, 95 {foth[94]},
                  96 {foth[95]}, 97 {foth[96]}, 98 {foth[97]}, 99 {foth[98]}, 100 {foth[99]}/
        iirf_horizon Time horizon for IIRF in yr                       /100/
        tocean0  two-layer "deep ocean" temperature change             /{t2*0.85/0.881}/
        tatm0    two-layer "surface" temperature change                /{t1}/
        fco22x   Forcing of equilibrium CO2 doubling (Wm-2)            /{cr[6]}/
        EBM_A11  Fast component of mixed layer temperature             /{cr[0]}/
        EBM_A12  Slow component of mixed layer temperature             /{cr[1]}/
        EBM_A21  Fast component of deep ocean temperature              /{cr[2]}/
        EBM_A22  Slow component of deep ocean temperature              /{cr[3]}/
        EBM_B1   Forcing contribution to mixed layer                   /{cr[4]}/
        EBM_B2   Forcing component to ocean layer                      /{cr[5]}/
** Climate damage parameters
        a10      Initial damage intercept                              /0/
        a20      Initial damage quadratic term
        a1       Damage intercept                                      /0/
        a2       Damage quadratic term                                 /0.00236/
        a3       Damage exponent                                       /2.00/
** Abatement cost
        expcost2  Exponent of control cost function                    /2.6/
        pback     Cost of backstop 2010$ per tCO2 2015                 /550/
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
        gfacpop(t)    Growth factor population
        pbacktime(t)  Backstop price
        optlrsav      Optimal long-run savings rate used for transversality
        scc(t)        Social cost of carbon
        cpricebase(t) Carbon price in base case
        photel(t)     Carbon Price under no damages (Hotelling rent condition)
        ppm(t)        Atmospheric concentrations parts per million
        atfrac2010(t) Atmospheric share since 2010;

* Program control definitions
        tfirst(t) = yes$(t.val eq 1);
        tlast(t)  = yes$(t.val eq card(t));
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
        l("1") = pop0;
        loop(t, l(t+1)=l(t););
        loop(t, l(t+1)=l(t)*(popasym/L(t))**popadj ;);

        ga(t)=ga0*exp(-dela*5*((t.val-1)));
        al("1") = a0; loop(t, al(t+1)=al(t)/((1-ga(t))););
        gsig("1")=gsigma1; loop(t,gsig(t+1)=gsig(t)*((1+dsig)**tstep) ;);
        sigma("1")=sig0;   loop(t,sigma(t+1)=(sigma(t)*exp(gsig(t)*tstep)););

        pbacktime(t)=pback*(1-gback)**(t.val-1);
        cost1(t) = pbacktime(t)*sigma(t)/expcost2/1000;

        etree(t) = eland0*(1-deland)**(t.val-1);
        cumetree("1")= 186.3; loop(t,cumetree(t+1)=cumetree(t)+etree(t)*(5/3.664););

        rr(t) = 1/((1+prstp)**(tstep*(t.val-1)));
        optlrsav = (dk + .004)/(dk + .004*elasmu + prstp)*gama;

* Base Case Carbon Price
        cpricebase(t)= cprice0*(1+gcprice)**(5*(t.val-1));

VARIABLES
        MIU(t)          Emission control rate GHGs
        FORC(t)         Increase in radiative forcing (watts per m2 from 1900)
        TATM(t)         Increase temperature of atmosphere (degrees C from 1900)
        TOCEAN(t)       Increase temperatureof lower oceans (degrees C from 1900)
        MAT(t)          Carbon concentration increase in atmosphere (GtC from 1750)
        MU(t)           Carbon concentration increase in shallow oceans (GtC from 1750)
        ML(t)           Carbon concentration increase in lower oceans (GtC from 1750)
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
        CCA(t)          Cumulative industrial carbon emissions (GTC)
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

NONNEGATIVE VARIABLES  MIU, TATM, MAT, MU, ML, Y, YGROSS, C, K, I, alpha;

EQUATIONS
*Emissions and Damages
        EEQ(t)          Emissions equation
        EINDEQ(t)       Industrial emissions
        CCACCA(t)       Cumulative industrial carbon emissions
        CCATOTEQ(t)     Cumulative total carbon emissions
        FORCE(t)        Radiative forcing equation
        DAMFRACEQ(t)    Equation for damage fraction
        DAMEQ(t)        Damage equation
        ABATEEQ(t)      Cost of emissions reductions equation
        MCABATEEQ(t)    Equation for MC abatement
        CARBPRICEEQ(t)  Carbon price equation from abatement

*Climate and carbon cycle
        MMAT(t)          Atmospheric concentration equation
        ATFRACEQ(t)      Atmospheric airborne fraction equation
        TATMEQ(t)        Temperature-climate equation for atmosphere
        TOCEANEQ(t)      Temperature-climate equation for lower oceans
        ALPHAEQ(t)       Scale factor equation
        IIRFEQ(t)        IIRF equation
        CBOX1EQ(t)       Carbon box 1 equation
        CBOX2EQ(t)       Carbon box 2 equation
        CBOX3EQ(t)       Carbon box 3 equation
        CBOX4EQ(t)       Carbon box 4 equation
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
 ccacca(t+1)..        CCA(t+1)       =E= CCA(t)+ EIND(t)*tstep/3.664;
 ccatoteq(t)..        CCATOT(t)      =E= CCA(t)+cumetree(t);
 force(t)..           FORC(t)        =E= fco22x * ((log((MAT(t)/mateq))/log(2))) + forcoth(t);
 damfraceq(t) ..      DAMFRAC(t)     =E= (a1*TATM(t))+(a2*TATM(t)**a3) ;
 dameq(t)..           DAMAGES(t)     =E= YGROSS(t) * DAMFRAC(t);
 abateeq(t)..         ABATECOST(t)   =E= YGROSS(t) * cost1(t) * (MIU(t)**expcost2);
 mcabateeq(t)..       MCABATE(t)     =E= pbacktime(t) * MIU(t)**(expcost2-1);
 carbpriceeq(t)..     CPRICE(t)      =E= pbacktime(t) * (MIU(t))**(expcost2-1);

* Climate and carbon cycle
 atfraceq(t)..        atfrac(t)      =E= ((mat(t)-mateq)/(ccatot(t)+0.0000001));
 iirfeq(t)..          IIRF(t)        =E= r0 + rc * (1-atfrac(t)) * ccatot(t) + rt * tatm(t);
 alphaeq(t)..         ALPHA(t)       =E= g0 * exp(iirf(t)/g1);
 cbox1eq(t+1)..       CBOX1(t+1)     =E= a("1")*E(t)*tstep/3.664 + cbox1(t) * exp(-tstep/(alpha(t)*tau("1")));
 cbox2eq(t+1)..       CBOX2(t+1)     =E= a("2")*E(t)*tstep/3.664 + cbox2(t) * exp(-tstep/(alpha(t)*tau("2")));
 cbox3eq(t+1)..       CBOX3(t+1)     =E= a("3")*E(t)*tstep/3.664 + cbox3(t) * exp(-tstep/(alpha(t)*tau("3")));
 cbox4eq(t+1)..       CBOX4(t+1)     =E= a("4")*E(t)*tstep/3.664 + cbox4(t) * exp(-tstep/(alpha(t)*tau("4")));
 tatmeq(t+1)..        TATM(t+1)      =E= EBM_A11 * TATM(t) + EBM_A12 * TOCEAN(t) + EBM_B1 * FORC(t);
 toceaneq(t+1)..      TOCEAN(t+1)    =E= EBM_A21 * TATM(t) + EBM_A22 * TOCEAN(t) + EBM_B2 * FORC(t);
 mmat(t)..            MAT(t)         =E= mateq + cbox1(t) + cbox2(t) + cbox3(t) + cbox4(t);
* constrainT(t)..      TATM(t)        =L= 2;

* Economic variables
 ygrosseq(t)..        YGROSS(t)      =E= (al(t)*(L(t)/1000)**(1-GAMA))*(K(t)**GAMA);
 yneteq(t)..          YNET(t)        =E= YGROSS(t)*(1-damfrac(t));
 yy(t)..              Y(t)           =E= YNET(t) - ABATECOST(t);
 cc(t)..              C(t)           =E= Y(t) - I(t);
 cpce(t)..            CPC(t)         =E= 1000 * C(t) / L(t);
 seq(t)..             I(t)           =E= S(t) * Y(t);
 kk(t+1)..            K(t+1)         =L= (1-dk)**tstep * K(t) + tstep * I(t);
 rieq(t+1)..          RI(t)          =E= (1+prstp) * (CPC(t+1)/CPC(t))**(elasmu/tstep) - 1;

* Utility
 cemutotpereq(t)..    CEMUTOTPER(t)  =E= PERIODU(t) * L(t) * rr(t);
 periodueq(t)..       PERIODU(t)     =E= ((C(T)*1000/L(T))**(1-elasmu)-1)/(1-elasmu)-1;
 util..               UTILITY        =E= tstep * scale1 * sum(t,  CEMUTOTPER(t)) + scale2 ;

* Resource limit
CCA.up(t)             = fosslim;
CCA.lo(t)             = 0;

* Control rate limits
MIU.up(t)             = limmiu;
MIU.up(t)$(t.val<30)  = 1;

** Upper and lower bounds for stability
K.LO(t)         = 1;
EIND.LO(t)      = -50;
MAT.LO(t)       = 10;
MU.LO(t)        = 100;
ML.LO(t)        = 1000;
C.LO(t)         = 2;
TOCEAN.UP(t)    = 20;
TOCEAN.LO(t)    = -1;
TATM.UP(t)      = 20;
CPC.LO(t)       = .01;
TATM.UP(t)      = 12;
IIRF.UP(t)      = 97;
IIRF.LO(t)      = 16;
alpha.lo(t)     = 0.01;
alpha.up(t)     = 100;

* Control variables
set lag10(t) ;
lag10(t) =  yes$(t.val gt card(t)-10);
S.FX(lag10(t)) = optlrsav;

* Initial conditions
CCA.FX(tfirst)    = 420.4902535;
K.FX(tfirst)      = k0;
MAT.FX(tfirst)     = mat0;
TATM.FX(tfirst)   = tatm0;
TOCEAN.FX(tfirst) = tocean0;
IIRF.l(tfirst)    = 50;
atfrac.l(tfirst)  = 0.526;
alpha.l(tfirst)   = 0.81;
*these three lines above need a check
cbox1.fx(tfirst)  = icbox1;
cbox2.fx(tfirst)  = icbox2;
cbox3.fx(tfirst)  = icbox3;
cbox4.fx(tfirst)  = icbox4;

** Solution options
option iterlim = 99900;
option reslim  = 99999;
option solprint = on;
option limrow = 0;
option limcol = 0;
model  CO2 /all/;

* For base run, this subroutine calculates Hotelling rents
* Carbon price is maximum of Hotelling rent or baseline price
* The cprice equation is different from 2013R. Not sure what went wrong.
If (ifopt eq 0,
       a2 = 0;
       solve CO2 maximizing UTILITY using nlp;
       photel(t)=cprice.l(t);
       a2 = a20;
      cprice.up(t)$(t.val<tnopol+1) = max(photel(t),cpricebase(t));
);

miu.fx('1')$(ifopt=1) = miu0;
solve co2 maximizing utility using nlp;
solve co2 maximizing utility using nlp;
solve co2 maximizing utility using nlp;

** POST-SOLVE
* Calculate social cost of carbon and other variables
scc(t)        = -1000*eeq.m(t)/(.00001+cc.m(t));
atfrac2010(t) = ((mat.l(t)-mat0)/(.00001+ccatot.l(t)-ccatot.l('1')  ));
ppm(t)        = mat.l(t)/2.124;

* Produces a file "Dice2016R-091916ap.csv" in the base directory
* For ALL relevant model outputs, see 'PutOutputAllT.gms' in the Include folder.
* The statement at the end of the *.lst file "Output..." will tell you where to find the file.

file results /"{here}/../data_output/dice/{run:04d}.csv"/; results.nd = 10 ; results.nw = 0 ; results.pw=20000; results.pc=5;
put results;
put // "Period";
Loop (T, put T.val);
put / "Year" ;
Loop (T, put (2010+(TSTEP*T.val) ));
put / "Industrial Emissions GTCO2 per year" ;
Loop (T, put EIND.l(T));
put / "Atmospheric concentrations ppm" ;
Loop (T, put ppm(t));
put / "Atmospheric Temperature rel. 1850-1900" ;
Loop (T, put TATM.l(T));
put / "Ocean Temperature rel. 1850-1900" ;
Loop (T, put TOCEAN.l(T));
put / "Output Net Net) " ;
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
Loop (T, put mat.l(t));
put / "Total Emissions GTCO2 per year" ;
Loop (T, put E.l(T));
put / "Atmospheric fraction since 1850" ;
Loop (T, put atfrac.l(t));
put / "Atmospheric fraction since 2010" ;
Loop (T, put atfrac2010(t));
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
    with open(os.path.join(here, 'gams_scripts', f'run{run:04d}.gms'), 'w') as f:
        f.write(template)

    # run the command
    with open(os.path.join(here, 'gams_scripts', f'run{run:04d}.out'), "w") as outfile:
        subprocess.run(
            [
                'gams',
                os.path.join(
                    here,
                    'gams_scripts',
                    f'run{run:04d}.gms'
                ),
                '-o',
                os.path.join(
                    here,
                    'gams_scripts',
                    f'run{run:04d}.lst'
                ),
            ],
            stdout = outfile,
        )

    # were results feasible?
    with open(os.path.join(here, 'gams_scripts', f'run{run:04d}.lst')) as f:
        output = f.read()
        if " ** Infeasible solution. Reduced gradient less than tolerance." in output:
            raise InfeasibleSolutionError(run)
