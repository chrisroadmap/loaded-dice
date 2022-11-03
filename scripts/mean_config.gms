
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
        q0       Initial world gross output 2020 (trill 2020 USD)      /133.09357438648962/
        k0       Initial capital value 2019                            /341.0027556142761/
        a0       Initial level of total factor productivity            /5.517123167924143/
        ga0      Initial growth rate for TFP per 5 years               /0.076/
        dela     Decline rate of TFP per 5 years                       /0.005/
        l(t)     /1 7.752698915999999, 2 8.14501447446709, 3 8.514264439238291, 4 8.851171048047874, 5 9.160805469777193,
                  6 9.443190102601223, 7 9.696205729551343, 8 9.924312962725988, 9 10.1235280089845, 10 10.29655254704842,
                 11 10.446114240546027, 12 10.577151930864575, 13 10.69672242725059, 14 10.802836907197488, 15 10.892777138932376,
                 16 10.97441664735782, 17 11.027833874574439, 18 11.088841944758256, 19 11.122549645864144, 20 11.148017580095328,
                 21 11.157324625053421, 22 11.172117316134777, 23 11.182142206294424, 24 11.169412682818685, 25 11.142629933116396,
                 26 11.116998728164878, 27 11.088723841450147, 28 11.05115858627234, 29 11.02205639000708, 30 10.939823540726353,
                 31 10.868377771775208, 32 10.792557027171881, 33 10.701633030064261, 34 10.606255631421268, 35 10.489725006178455,
                 36 10.394377066405719, 37 10.280836858083662, 38 10.180553974334368, 39 10.08030953089341, 40 9.929925720534952,
                 41 9.822382252063436, 42 9.686034776542154, 43 9.530377328345775, 44 9.388706123064578, 45 9.244220068798658,
                 46 9.073130986446273, 47 8.93002080192914, 48 8.72914878001665, 49 8.582313506050513, 50 8.3887527173362,
                 51 8.252671482044136, 52 8.128437203454254, 53 7.948013848638106, 54 7.77978011325613, 55 7.5981793053525255,
                 56 7.440134526590741, 57 7.303497749693029, 58 7.212186062493577, 59 7.065115310826582, 60 6.959244141597544,
                 61 6.822626293068621, 62 6.6975574796010635, 63 6.578123629290501, 64 6.466998205985376, 65 6.350788991834326,
                 66 6.2675317054356645, 67 6.178043698130286, 68 6.109378900494941, 69 6.046847533102705, 70 5.989084145464406,
                 71 5.896942424664613, 72 5.838078741820963, 73 5.768980668470196, 74 5.69520012860349, 75 5.6355584252569715,
                 76 5.574713099792021, 77 5.516546578050418, 78 5.44356701288864, 79 5.383449787086264, 80 5.338821988347904,
                 81 5.290319253858154, 82 5.246486909426832, 83 5.200206967292477, 84 5.1633241426111915, 85 5.1404253544505805,
                 86 5.104915636293876, 87 5.075824595714507, 88 5.049124354407201, 89 5.024777879641999, 90 5.00473099716016,
                 91 4.9898701739085105, 92 4.976699777294193, 93 4.965206097266192, 94 4.955377124072447, 95 4.947202527361643,
                 96 4.94067363811745, 97 4.935783433381051, 98 4.932526523724367, 99 4.930899143442817, 100 4.930899143442817/
** Emissions parameters
        gsigma1  Initial growth of sigma (per year)                    /-0.0152/
        dsig     Decline rate of decarbonization (per period)          /-0.001/
        e0       Industrial emissions 2020 (GtCO2 per year)            /36.70/
* projections from RCMIP (should use GCP; TODO)
        miu0     Initial emissions control rate for base case 2015     /0.15/
* Initial Conditions
        co2_2020 Initial concentration in atmosphere 2020 (GtC)        /877.7022270912074/
        co2_1750 Pre-industrial concentration atmosphere  (GtC)        /591.9851790277355/
* These are for declaration and are defined later
        sig0     Carbon intensity 2010 (kgCO2 per output 2005 USD 2010)
** Climate model parameters
        g0       Carbon cycle parameter (Leach et al. 2021)
        g1       Carbon cycle parameter (Leach et al. 2021)
        r0       Pre-industrial time-integrated airborne fraction      /33.707991262815256/
        ru       Sensitivity of airborne fraction with CO2 uptake      /0.003426378858380945/
        rt       Sensitivity of airborne fraction with temperature     /2.3665473196484275/
        ra       Sensitivity of airborne fraction with CO2 airborne    /0.0016877120877617834/
        tau(box) Lifetimes of the four atmospheric carbon boxes
                     / 1 1e9, 2 394.4, 3 36.54, 4 4.304 /
        a(box)   Partition fraction of the four atmospheric carbon boxes
                     / 1 0.2173, 2 0.2240, 3 0.2824, 4 0.2763 /
        ICBOX1   Initial GtC concentration of carbon box 1 in 2020     /142.19968408720618/
        ICBOX2   Initial GtC concentration of carbon box 2 in 2020     /101.89205189742611/
        ICBOX3   Initial GtC concentration of carbon box 3 in 2020     /36.31600258734868/
        ICBOX4   Initial GtC concentration of carbon box 4 in 2020     /5.3093094914908034/
        iirf_horizon Time horizon for IIRF in yr                       /100/
        t1_0     three-layer "mixed layer" temperature change          /1.234630030608191/
        t2_0     three-layer "mid-ocean" temperature change            /0.837054554415475/
        t3_0     three-layer "deep-ocean" temperature change           /0.27964187504557875/
        EBM_A11  Fast component of mixed layer temperature             /0.07790134885533427/
        EBM_A12  Intermediate component of mixed layer temperature     /0.36529270554362925/
        EBM_A13  Slow component of mixed layer temperature             /0.13965825404191443/
        EBM_A21  Fast component of mid ocean temperature               /0.08189096365651416/
        EBM_A22  Intermediate component of mid ocean temperature       /0.528413520955148/
        EBM_A23  Slow component of mid ocean temperature               /0.2365989107612785/
        EBM_A31  Fast component of deep ocean temperature              /0.008316076511537767/
        EBM_A32  Intermediate component of deep ocean temperature      /0.07334669905622317/
        EBM_A33  Slow component of deep ocean temperature              /0.9109931044425426/
        EBM_B1   Forcing contribution to mixed layer                   /0.3161368340237162/
        EBM_B2   Forcing component to ocean layer                      /0.11763985620815468/
        EBM_B3   Forcing component to ocean layer                      /0.005519163787478726/
        fco22x   Forcing of equilibrium CO2 doubling (Wm-2)            /3.8633934259285456/
        nonco2(t)   /1 0.548764861085623, 2 0.62779968624629, 3 0.6483240141633643, 4 0.6918405477540968, 5 0.7408862970332162,
                  6 0.7845687915811056, 7 0.8291958706223516, 8 0.8599012544046831, 9 0.8725489133539992, 10 0.8798256220258514,
                 11 0.8962575121154778, 12 0.9108179023131088, 13 0.9292868682978804, 14 0.9504946766795525, 15 0.9821086020829756,
                 16 1.0076120937244264, 17 1.022197027249214, 18 1.0304248034239123, 19 1.0209018149210425, 20 1.0116817770351925,
                 21 0.998265134324503, 22 0.9854958704470228, 23 0.9700138267308556, 24 0.9571180055822844, 25 0.9420814185982762,
                 26 0.923732559253472, 27 0.9074502936738412, 28 0.889748721481196, 29 0.870683800569012, 30 0.852442630676264,
                 31 0.8346016975092663, 32 0.818568149331568, 33 0.8013079425124926, 34 0.7846344486269217, 35 0.7681270020695166,
                 36 0.7494849880108287, 37 0.7329997154655866, 38 0.7179576688895952, 39 0.7004543325002993, 40 0.6838046432409213,
                 41 0.6680913095417442, 42 0.6524114917154806, 43 0.6389962379807582, 44 0.6252596473235126, 45 0.6117713094057634,
                 46 0.5968737413461513, 47 0.5838335358959111, 48 0.5687573395620079, 49 0.5559684666868545, 50 0.5466900286870682,
                 51 0.5391900455032282, 52 0.5332787564791356, 53 0.5282234277473258, 54 0.5240161113962621, 55 0.5204350837772741,
                 56 0.5170742196083405, 57 0.5143288302480931, 58 0.5121896862619356, 59 0.5100269144497417, 60 0.5080894510901026,
                 61 0.5063220959896763, 62 0.5050381944133702, 63 0.5037405105506219, 64 0.5025597619165167, 65 0.5014840749676539,
                 66 0.5005032150808204, 67 0.499632452871388, 68 0.4987913256833068, 69 0.4980454592192594, 70 0.4972400674234712,
                 71 0.4964277648046983, 72 0.4956711647994954, 73 0.4951008282426233, 74 0.4946137692364994, 75 0.4937175860797794,
                 76 0.4928627843244743, 77 0.4920785791168179, 78 0.4916753556222427, 79 0.4913041936862435, 80 0.4908925320761154,
                 81 0.4902920416857083, 82 0.4900826643682759, 83 0.4897630533525133, 84 0.4893242070094218, 85 0.4889052442590381,
                 86 0.4885049166531846, 87 0.488440637905942, 88 0.4884307994528227, 89 0.4878371401686394, 90 0.4874089819117425,
                 91 0.4874412366159367, 92 0.4874845164594742, 93 0.4875379060246568, 94 0.4873799373257282, 95 0.487225014257476,
                 96 0.4870810672463092, 97 0.4869474664100081, 98 0.4869474664100081, 99 0.4869474664100081, 100 0.4869474664100081/
** Climate damage parameters
        a10      Initial damage intercept                              /0/
        a20      Initial damage quadratic term
        a1       Damage intercept                                      /0/
        a2       Damage quadratic term                                 /0.00236/
        a3       Damage exponent                                       /2.00/
** Abatement cost
        expcost2  Exponent of control cost function                    /2.6/
        pback     Cost of backstop 2020$ per tCO2 2015                 /679/
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
        gl(t)         Growth rate of labor
        gcost1        Growth of cost factor
        gsig(t)       Change in sigma (cumulative improvement of energy efficiency)
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
        tearly(t) = yes$(t.val le 17);
        tlate(t)  = yes$(t.val gt 17);
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
 forceq(t)..          FORC(t)        =E= fco22x * ((log((CO2(t)/co2_1750))/log(2))) + nonco2(t);
 damfraceq(t) ..      DAMFRAC(t)     =E= (a1*T1(t))+(a2*T1(t)**a3) ;
 dameq(t)..           DAMAGES(t)     =E= YGROSS(t) * DAMFRAC(t);
 abateeq(t)..         ABATECOST(t)   =E= YGROSS(t) * cost1(t) * (MIU(t)**expcost2);
 mcabateeq(t)..       MCABATE(t)     =E= pbacktime(t) * MIU(t)**(expcost2-1);
 carbpriceeq(t)..     CPRICE(t)      =E= pbacktime(t) * (MIU(t))**(expcost2-1);
 etreeeq(t)..         etree(t)       =e= (0.5185672924533753 + (0.045401592070056)*EIND(t) + (-0.267725213334951)*t.val) * (1 - 1/(1+exp(-0.75*(t.val-22))));
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
cumetree.fx(tfirst) = 190.9;

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
ppm(t)        = co2.l(t)/2.1290606558508802;

* Produces a file "Dice2016R-091916ap.csv" in the base directory
* For ALL relevant model outputs, see 'PutOutputAllT.gms' in the Include folder.
* The statement at the end of the *.lst file "Output..." will tell you where to find the file.

file results /"mean_config.csv"/; results.nd = 10 ; results.nw = 0 ; results.pw=20000; results.pc=5;
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
put / "Objective" ;
put utility.l;
putclose;
