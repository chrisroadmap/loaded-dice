$ontext
DICE2022-beta-3-17-3.gms
May 15, 2023
Includes all revisions and the final damage update
Replaces beta-3 version DICE2022-beta.3-17-1p.gms
Slight revision of treatment of beta and K0
$offtext

$title        May 15, 2022 (DICE2022-beta-3-17-3.gms)

set        t  Time periods (5 years per period)                     /1*101/

PARAMETERS
** If optimal control
        ifopt    Indicator where optimized is 1 and base is 0        /1/
        
** Population and technology
        gama     Capital elasticity in production function        /.300    /
        pop0     Initial world population 2020 (millions)         /7752.9  /
        popadj   Growth rate to calibrate to 2050 pop projection  /0.145   /
        popasym  Asymptotic population (millions)                 /10825.  /
        dk       Depreciation rate on capital (per year)          /.100    /
        q0       Initial world output 2020 (trill 2019 USD)       /135.7   /
        A0       Initial level of total factor productivity       /5.84164 /
        gA0      Initial growth rate for TFP per 5 years          /0.082   /
        delA     Decline rate of TFP per 5 years                  /0.0072  /
        k0       Initial K 2020 for beta = 0.6 (trill 2019 USD)   / 302  /
** Emissions parameters and Non-CO2 GHG
        gsigma1   Initial growth of sigma (per year)                   / -0.015 /
        delgsig   Decline rate of gsigma per period                    /.96/
        asymgsig   Asympototic gsigma                                  /-.005/ 
        e0        Industrial emissions 2020 (GtCO2 per year)           / 37.56  /
        miu0      Emissions control rate historical 2020               / .05    /
        fosslim   Maximum cumulative extraction fossil fuels (GtC)     / 6000   /
        CumEmiss0 Cumulative emissions 2020 (GtC)                      / 633.5379/
* Climate damage parameters
        a10       Initial damage intercept                            /0      /
        a1        Damage intercept                                    /0      /
        a2base    Damage quadratic term rev 01-13-23                  /0.003467/
        a3        Damage exponent                                     /2.00   /
** Abatement cost
        expcost2  Exponent of control cost function                   / 2.6  /
        pback2050 Cost of backstop 2019$ per tCO2 2050                / 515.  /
        gback     Initial cost decline backstop cost per year         / -.012 /
        delgback  Decline factor of gback per period                  /.95/
        cprice0   Carbon price 2020 2019$ per tCO2                    / 6    /
        gcprice   Growth rate of base carbon price per year           /.01   /      
** Limits on emissions controls
        limmiu2070     
        limmiu2120    
        delmiumax     
** Preferences and timing
        betaclim                                                    / 0.6  /
        elasmu    Elasticity of marginal utility of consumption     / 0.9  /
        rhof      Riskfree real rate per year                       / .001 /
        rhok      Rate of risky social time preference per year     / .035 /
        prstp
** For redefinitions, not numerical
        a20       Initial damage quadratic term
        a2        Damage in program
        sig0      Carbon intensity 2020 (kgCO2 per output 2020 USD 2019 no policy)
** Scaling so that MU(C(1)) = 1 and objective function = PV consumption
        tstep       Years per Period                               / 5  /
        scale1      Multiplicative scaling coefficient             /0.009889 /
        scale2      Additive scaling coefficient                   /-7776.944399/ ;
** Other calibration parameters
        a2 = a2base;
        prstp = rhof+rhoK*betaclim;
* Program control variables
sets     tfirst(t), tlast(t), tearly(t), tlate(t);

PARAMETERS
        L(t)           Level of population and labor
        aL(t)          Level of total factor productivity
        sigma(t)       CO2-emissions output ratio
        sigmatot(t)    GHG-output ratio
        RR(t)          Average utility social discount rate
        gA(t)          Growth rate of productivity from
        gL(t)          Growth rate of labor and population
        gcost1         Growth of cost factor
        gsig(t)        Change in sigma (rate of decarbonization)
        eland(t)       Emissions from deforestation (GtCO2 per year)
        cost1tot(T)    Abatement cost adjusted for backstop and sigma
        pbacktime(t)   Backstop price 2019$ per ton CO2
        optlrsav       Optimal long-run savings rate used for transversality
        scc(t)         Social cost of carbon
        cpricebase(t)  Carbon price in base case
        photel(t)      Carbon Price under no damages (Hotelling rent condition)
        ppm(t)         Atmospheric concentrations parts per million
        atfrac2020(t)  Atmospheric share since 2020
        atfrac1765(t)  Atmospheric fraction of emissions since 1765
        abaterat(t)    Abatement cost per net output
        miuup(t)       Upper bound on miu
        gbacktime(t)   Decline rate of backstop price
;
** Dynamic parameter values        
        L("1") = pop0; loop(t, L(t+1)=L(t););
        loop(t, L(t+1)=L(t)*(popasym/L(t))**popadj ;);
        gA(t)=gA0*exp(-delA*5*((t.val-1)));
        aL("1") = A0; loop(t, aL(t+1)=aL(t)/((1-gA(t))););
        RR(t) = 1/((1+prstp)**(tstep*(t.val-1)));
        optlrsav = (dk + .004)/(dk + .004*elasmu + prstp)*gama;
        cpricebase(t)= cprice0*(1+gcprice)**(5*(t.val-1));

        gbacktime(t)=gback*delgback**((t.val-1));
        pbacktime(t)=pback2050*exp(-5*(.01)*(t.val-7));
        pbacktime(t)$(t.val > 7) = pback2050*exp(-5*(.001)*(t.val-7));
        sig0 = e0/(q0*(1-miu0));  
        sigma("1")=sig0;
        gsig(t)=min(gsigma1*delgsig **((t.val-1)),asymgsig);
        loop(t, sigma(t+1)=sigma(t)*exp(5*gsig(t)););       
** Emissions limits
        limmiu2070 = 1;     
        limmiu2120 = 1.1;   
        delmiumax = 0.12;          
        miuup('1')= .05;
        miuup('2')= .10;
        miuup(t)$(t.val > 2) = ( delmiumax*(t.val-1));
        miuup(t)$(t.val > 8) = 0.85+.05*(t.val-8);
        miuup(t)$(t.val > 11) = limmiu2070;        
        miuup(t)$(t.val > 20) = limmiu2120;
** Include file for non-CO2 GHGs        
$include Include/Nonco2-b-3-17.gms
       
* Program control definitions
        tfirst(t) = yes$(t.val eq 1);
        tlast(t)  = yes$(t.val eq card(t));
        
VARIABLES
        MIU(t)          Emission control rate GHGs
        C(t)            Consumption (trillions 2019 US dollars per year)
        K(t)            Capital stock (trillions 2019 US dollars)
        CPC(t)          Per capita consumption (thousands 2019 USD per year)
        I(t)            Investment (trillions 2019 USD per year)
        S(t)            Gross savings rate as fraction of gross world product
        RI(t)           Real interest rate (per annum)
        Y(t)            Gross world product net of abatement and damages (trillions 2019 USD per year)
        YGROSS(t)       Gross world product GROSS of abatement and damages (trillions 2019 USD per year)
        YNET(t)         Output net of damages equation (trillions 2019 USD per year)
        DAMAGES(t)      Damages (trillions 2019 USD per year)
        DAMFRAC(t)      Damages as fraction of gross output
        ABATECOST(t)    Cost of emissions reductions  (trillions 2019 USD per year)
        MCABATE(t)      Marginal cost of abatement (2019$ per ton CO2)
        CCATOT(t)       Total carbon emissions (GtC)
        PERIODU(t)      One period utility function
        CPRICE(t)       Carbon price (2019$ per ton of CO2)
        CEMUTOTPER(t)   Period utility
        UTILITY         Welfare function
;
NONNEGATIVE VARIABLES  MIU, TATM, MAT, MU, ML, Y, YNET, YGROSS, C, K, I;
EQUATIONS
*Emissions and Damages
        CCATOTEQ(t)      Cumulative total carbon emissions
        DAMFRACEQ(t)     Equation for damage fraction
        DAMEQ(t)         Damage equation
        ABATEEQ(t)       Cost of emissions reductions equation
        MCABATEEQ(t)     Equation for MC abatement
        CARBPRICEEQ(t)   Carbon price equation from abatement
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
        UTIL             Objective function      ;
      
** Include file for DFAIR model and climate equations
$include Include/FAIR-beta-3-17.gms

** Equations of the model
**Emissions and Damages
 eco2eq(t)..          ECO2(t)        =E= (sigma(t)*YGROSS(t) + eland(t))*(1-(MIU(t)));
 eindeq(t)..          EIND(t)        =E= (sigma(t)*YGROSS(t))*(1-(MIU(t)));
 eco2Eeq(t)..         ECO2E(t)       =E= (sigma(t)*YGROSS(t) + eland(t) + CO2E_GHGabateB(t))*(1-(MIU(t)));
 F_GHGabateEQ(t+1)..  F_GHGabate(t+1) =E= Fcoef2*F_GHGabate(t)+ Fcoef1*CO2E_GHGabateB(t)*(1-(MIU(t)));
 ccatoteq(t+1)..      CCATOT(t+1)    =E= CCATOT(t) +  ECO2(T)*(5/3.666) ;
 damfraceq(t) ..      DAMFRAC(t)     =E= (a1*(TATM(t)))+(a2*(TATM(t))**a3) ;
 dameq(t)..           DAMAGES(t)     =E= YGROSS(t) * DAMFRAC(t);
 abateeq(T)..         ABATECOST(T)   =E= YGROSS(T) * COST1TOT(T) * (MIU(T)**EXPCOST2);
 mcabateeq(t)..       MCABATE(t)     =E= pbacktime(t) * MIU(t)**(expcost2-1);
 carbpriceeq(t)..     CPRICE(t)      =E= pbacktime(t) * (MIU(t))**(expcost2-1);
**Economic variables
 ygrosseq(t)..        YGROSS(t)      =E= (aL(t)*(L(t)/1000)**(1-gama))*(K(t)**gama);
 yneteq(t)..          YNET(t)        =E= YGROSS(t)*(1-damfrac(t));
 yy(t)..              Y(t)           =E= YNET(t) - ABATECOST(t);
 cc(t)..              C(t)           =E= Y(t) - I(t);
 cpce(t)..            CPC(t)         =E= 1000 * C(t) / L(t);
 seq(t)..             I(t)           =E= S(t) * Y(t);
 kk(t+1)..            K(t+1)         =L= (1-dk)**tstep * K(t) + tstep * I(t);
 rieq(t+1)..          RI(t)          =E= (1+prstp) * (CPC(t+1)/CPC(t))**(elasmu/tstep) - 1;
**Utility and objective function
 cemutotpereq(t)..    CEMUTOTPER(t)  =E= PERIODU(t) * L(t) * RR(t);
 periodueq(t)..       PERIODU(t)     =E= ((C(T)*1000/L(T))**(1-elasmu)-1)/(1-elasmu)-1;
 util..               UTILITY        =E= tstep * scale1 * sum(t,  CEMUTOTPER(t)) + scale2 ;

* Ccntrol rate limits
miu.up(t) = miuup(t);
K.LO(t)         = 1;
C.LO(t)         = 2;
CPC.LO(t)       = .01;

*Control for terminal savings rate
set lag10(t) ;
lag10(t) =  yes$(t.val gt card(t)-10);
S.FX(lag10(t)) = optlrsav;
ri.fx(tlast) = .014;

* Initial conditions
ccatot.fx(tfirst) = CumEmiss0;
k.FX(tfirst)      = k0;
F_GHGabate.fx(tfirst) = F_GHGabate2020;

** Solution options
option iterlim = 99900;
option reslim = 99999;
option solprint = on;
option limrow = 0;
option limcol = 0;
model  CO2 /all/;

* Initialize with optimal run
ifopt=1;
solve CO2 maximizing UTILITY using nlp ;

**** STATMENTS FOR DEFINITIONS AND PUT STATEMENTS FOR SCENARIOS 
*OPTIMAL
$include Include/def-opt-b-3-17.gms
$include Include/put-b-3-17-3.gms
$include Include/put-opt-b-3-17.gms
$include Include/put_list_module-b-3-17.gms

* 2 DEGREE LIMIT
$include Include/def-T2-b-3-17.gms
$include Include/put-T2-b-3-17.gms
$include Include/put_list_module-b-3-17.gms

* 1.5 DEGREE LIMIT
$include Include/def-T15-b-3-17.gms
$include Include/put-T15-b-3-17.gms
$include Include/put_list_module-b-3-17.gms
 
* Alternative damages
$include Include/def-altdam-b-3-17.gms
$include Include/put-altdam-b-3-17.gms
$include Include/put_list_module-b-3-17.gms

* PARIS ACCORD AS OF 2022
$include Include/def-paris-b-3-17.gms
$include Include/put-PARIS-b-3-17.gms
$include Include/put_list_module-b-3-17.gms

* BASELINE WITH CURRENT LEVEL OF POLICY 
$include Include/def-base-b-3-17.gms
$include Include/put-base-b-3-17.gms
$include Include/put_list_module-b-3-17.gms

* 5% DISCOUNT RATE
$include Include/def_DISC5%-b-3-17.gms
$include Include/put-DISC5%-b-3-17.gms
$include Include/put_list_module-b-3-17.gms

* 4% DISCOUNT RATE
$include Include/def_DISC4%-b-3-17.gms
$include Include/put-DISC4%-b-3-17.gms
$include Include/put_list_module-b-3-17.gms

* 3% DISCOUNT RATE 
$include Include/def_DISC3%-b-3-17.gms
$include Include/put-DISC3%-b-3-17.gms
$include Include/put_list_module-b-3-17.gms

* 2% DISCOUNT RATE
$include Include/def_DISC2%-b-3-17.gms
$include Include/put-DISC2%-b-3-17.gms
$include Include/put_list_module-b-3-17.gms

* 1% DISCOUNT RATE
$include Include/def_DISC1%-b-3-17.gms
$include Include/put-DISC1%-b-3-17.gms
$include Include/put_list_module-b-3-17.gms

*DISPLAY FOR MAJOR VARIABLES
option decimals = 5;
display cc.m,kk.m,cost1tot, pbacktime, sigmatot,miuup;
display gbacktime,gsig,sigma,s.l,k.l, eco2.l, eind.l,eco2e.l;
display miu.l, forc.l, mat.l, tatm.l,scc,ri.l,s.l,k.l;
display  ifopt, elasmu, prstp, k0, betaclim,rhok,rhof,k0,utility.l;
