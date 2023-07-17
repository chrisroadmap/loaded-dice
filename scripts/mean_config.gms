
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
        elasmu   Elasticity of marginal utility of consumption         /1.45/
        prstp    Initial rate of social time preference per year       /0.015/
** Technology and population (updated by CS)
        gama     Capital elasticity in production function             /0.300/
        dk       Depreciation rate on capital (per year)               /0.100/
        q0       Initial world gross output 2020 (trill 2020 USD)      /133.09357438648962/
        k0       Initial capital value 2019                            /341.0027556142761/
        a0       Initial level of total factor productivity            /5.4028103629527156/
        ga0      Initial growth rate for TFP per 3 years               /0.045/
        dela     Decline rate of TFP per 3 years                       /0.003/
        l(t)     /1 7.988088251080253, 2 8.219557765324929, 3 8.440416043973288, 4 8.649805513021741, 5 8.851171048047874,
                  6 9.03764944287387, 7 9.216889609640976, 8 9.387041158658047, 9 9.544738372360976, 10 9.696205729551343,
                 11 9.834688348182238, 12 9.961692239340886, 13 10.083764983814815, 14 10.190942946214331, 15 10.29655254704842,
                 16 10.387845477781728, 17 10.473043633259689, 18 10.550827155655554, 19 10.625159849891618, 20 10.69672242725059,
                 21 10.760310632680119, 22 10.821607491969688, 23 10.872651499412537, 24 10.924329404933914, 25 10.97441664735782,
                 26 11.00827330325542, 27 11.039691973943045, 28 11.078352293557343, 29 11.104676186852354, 30 11.122549645864144,
                 31 11.137677431718483, 32 11.153219763398546, 33 11.152831784211136, 34 11.165119816827008, 35 11.172117316134777,
                 36 11.175218583557823, 37 11.17378472874312, 38 11.168060761697209, 39 11.153577285801841, 40 11.142629933116396,
                 41 11.127001333818853, 42 11.12038645088574, 43 11.104510409276743, 44 11.058397503550564, 45 11.05115858627234,
                 46 11.034926187219686, 47 10.996948960409744, 48 10.952535086999953, 49 10.91054522657011, 50 10.868377771775208,
                 51 10.818953271780169, 52 10.777201533863444, 53 10.718134841690683, 54 10.657382577233498, 55 10.606255631421268,
                 56 10.535857878455428, 57 10.466117448065495, 58 10.42018212410062, 59 10.345362223502901, 60 10.280836858083662,
                 61 10.235999675212188, 62 10.155723353950364, 63 10.098198315103005, 64 10.016325248938319, 65 9.929925720534952,
                 66 9.87808153233644, 67 9.801978930763712, 68 9.716681691185736, 69 9.61290175673765, 70 9.530377328345775,
                 71 9.444024454399871, 72 9.363918233320815, 73 9.27135860381585, 74 9.179040700825478, 75 9.073130986446273,
                 76 8.990951000354245, 77 8.877035331652452, 78 8.751179180330025, 79 8.688806858183712, 80 8.582313506050513,
                 81 8.470542689743697, 82 8.348068944131262, 83 8.26995468174115, 84 8.185125968763323, 85 8.128437203454254,
                 86 8.007063606827847, 87 7.910950500060649, 88 7.821116464356958, 89 7.728835184432587, 90 7.5981793053525255,
                 91 7.514568481504303, 92 7.397201518044275, 93 7.330280071906696, 94 7.27817968212724, 95 7.212186062493577,
                 96 7.132146502731247, 97 7.0345721126679255, 98 6.974907403392753, 99 6.904597002185975, 100 6.822626293068621,
                 101 6.744325313940573, 102 6.6708059908591695, 103 6.596753523429123, 104 6.536600329592642, 105 6.466998205985376,
                 106 6.3855403856097706, 107 6.334137534554594, 108 6.284183162715397, 109 6.232692107449714, 110 6.178043698130286,
                 111 6.137034911851794, 112 6.0973983946730375, 113 6.061456877207328, 114 6.020827122243718, 115 5.989084145464406,
                 116 5.936189700598368, 117 5.8842702949778225, 118 5.846595732660951, 119 5.81177029238532, 120 5.768980668470196,
                 121 5.729046058496419, 122 5.679166265509125, 123 5.64606939686716, 124 5.613632357277553, 125 5.574713099792021,
                 126 5.547020578715895, 127 5.494586385518065, 128 5.456310439541369, 129 5.41952012256769, 130 5.383449787086264,
                 131 5.350543916306668, 132 5.333520886190516, 133 5.297483130245309, 134 5.273984682345418, 135 5.246486909426832,
                 136 5.218894027914855, 137 5.191158464230827, 138 5.1669329883160255, 139 5.156581121697113, 140 5.1404253544505805,
                 141 5.117524542187811, 142 5.099097428178003, 143 5.0816428038303805, 144 5.065144499191585, 145 5.049124354407201,
                 146 5.0345164695480795, 147 5.020372592731726, 148 5.008044333964267, 149 4.9987866678595, 150 4.9898701739085105,
                 151 4.98196793593992, 152 4.974401041288593, 153 4.967504833271792, 154 4.961274507988694, 155 4.955377124072447,
                 156 4.950472366045965, 157 4.945896749512804, 158 4.941979415966289, 159 4.93871755622289, 160 4.935783433381051/
** Emissions parameters
        gsigma1  Initial growth of sigma (per year)                    /-0.0152/
        dsig     Decline rate of decarbonization (per period)          /-0.0006/
        e0       Industrial emissions 2023 (GtCO2 per year)            /36.64/
        miu0     Initial emissions control rate for base case 2023     /0.15/
* Initial Conditions
        co2_2023 Initial concentration in atmosphere 2023 (GtC)        /889.6215841022483/
        co2_1750 Pre-industrial concentration atmosphere  (GtC)        /591.7810164433978/
* These are for declaration and are defined later
        sig0     Carbon intensity 2023 (kgCO2 per output 2020 Int$)
** Climate model parameters
        g0       Carbon cycle parameter (Leach et al. 2021)
        g1       Carbon cycle parameter (Leach et al. 2021)
        r0       Pre-industrial time-integrated airborne fraction      /32.10158825990729/
        ru       Sensitivity of airborne fraction with CO2 uptake      /0.0025709655190405377/
        rt       Sensitivity of airborne fraction with temperature     /2.3205670338781785/
        ra       Sensitivity of airborne fraction with CO2 airborne    /0.002290070024078019/
        tau(box) Lifetimes of the four atmospheric carbon boxes
                     / 1 1e9, 2 394.4, 3 36.54, 4 4.304 /
        a(box)   Partition fraction of the four atmospheric carbon boxes
                     / 1 0.2173, 2 0.2240, 3 0.2824, 4 0.2763 /
        ICBOX1   Initial GtC concentration of carbon box 1 in 2023     /154.80699025731403/
        ICBOX2   Initial GtC concentration of carbon box 2 in 2023     /103.65360330389099/
        ICBOX3   Initial GtC concentration of carbon box 3 in 2023     /34.515326264151646/
        ICBOX4   Initial GtC concentration of carbon box 4 in 2023     /4.864647833493791/
        iirf_horizon Time horizon for IIRF in yr                       /100/
        t1_0     three-layer "mixed layer" temperature change          /1.3217087258339648/
        t2_0     three-layer "mid-ocean" temperature change            /0.8901262542015365/
        t3_0     three-layer "deep-ocean" temperature change           /0.25242275189858904/
        EBM_A11  Fast component of mixed layer temperature             /0.1525691518990131/
        EBM_A12  Intermediate component of mixed layer temperature     /0.41075085947083784/
        EBM_A13  Slow component of mixed layer temperature             /0.08901196369677765/
        EBM_A21  Fast component of mid ocean temperature               /0.10880921861469264/
        EBM_A22  Intermediate component of mid ocean temperature       /0.6264992567586621/
        EBM_A23  Slow component of mid ocean temperature               /0.17476982279015252/
        EBM_A31  Fast component of deep ocean temperature              /0.004277815623396934/
        EBM_A32  Intermediate component of deep ocean temperature      /0.031676952777009/
        EBM_A33  Slow component of deep ocean temperature              /0.9623122126201734/
        EBM_B1   Forcing contribution to mixed layer                   /0.27594238244645386/
        EBM_B2   Forcing component to ocean layer                      /0.07347283234164519/
        EBM_B3   Forcing component to ocean layer                      /0.0014600935311228757/
        fco22x   Forcing of equilibrium CO2 doubling (Wm-2)            /3.94256105774036/
        nonco2(t) /1 0.5062395535118053, 2 0.4672534870420284, 3 0.4969657363112773, 4 0.5189003607935598, 5 0.5509512735762399,
                  6 0.5806727673475266, 7 0.608566486901366, 8 0.635407214574107, 9 0.6662296122946605, 10 0.6910450069004832,
                 11 0.7096009145248594, 12 0.7195107413838917, 13 0.7279231795812748, 14 0.7376687768094027, 15 0.7467257009347795,
                 16 0.7539065955675102, 17 0.7665680626538482, 18 0.7826491204299053, 19 0.7957072758279987, 20 0.8147351053000724,
                 21 0.8330373159192823, 22 0.8552272538939667, 23 0.8825813893014571, 24 0.9073700141085916, 25 0.9197783351894552,
                 26 0.9323387874581786, 27 0.9462538133762552, 28 0.948013409036876, 29 0.9435721346260684, 30 0.9383890604458586,
                 31 0.932903030937617, 32 0.9265439811805954, 33 0.919734118651248, 34 0.9122658910375012, 35 0.9053073927529308,
                 36 0.8978816815413161, 37 0.8900056689156199, 38 0.8813892819528791, 39 0.8722983269413346, 40 0.8638596574590206,
                 41 0.8526417187729036, 42 0.8440974543885567, 43 0.8356032225448007, 44 0.8265219153847138, 45 0.815459919637655,
                 46 0.8060876563195022, 47 0.7974187637899991, 48 0.7868551421685388, 49 0.777194191132399, 50 0.768395258123439,
                 51 0.7581554606404145, 52 0.7488624724128589, 53 0.7387888896416535, 54 0.7288584869989043, 55 0.7190018612616057,
                 56 0.7094669962518336, 57 0.7003626896089096, 58 0.6913438784737392, 59 0.6825191237917329, 60 0.6740312867188266,
                 61 0.6647441657068874, 62 0.6546427126258093, 63 0.6454015217001822, 64 0.6373416096001231, 65 0.6285670526123847,
                 66 0.6199525313750462, 67 0.6102228005827431, 68 0.6020890879143806, 69 0.5929654204632725, 70 0.5849113358724363,
                 71 0.5776171777505743, 72 0.5695981272909169, 73 0.5625770099233395, 74 0.5543517695303647, 75 0.5455772125602218,
                 76 0.5369833045294871, 77 0.5305702189144224, 78 0.5212750388584957, 79 0.5124046444538104, 80 0.5051394801454849,
                 81 0.500283319480207, 82 0.4957768420329144, 83 0.4916274679586224, 84 0.4878886982945215, 85 0.4845509604167721,
                 86 0.4815595992388519, 87 0.479174919372374, 88 0.4770151685716881, 89 0.4750430064928521, 90 0.4732295391049874,
                 91 0.4715521858618123, 92 0.4700432281259512, 93 0.4685869918482337, 94 0.4672098186879088, 95 0.4658956878139439,
                 96 0.4646646636353908, 97 0.4634854362286276, 98 0.4623021875125082, 99 0.4606361120380502, 100 0.4594921641085668,
                 101 0.4585228908861196, 102 0.4577889517659128, 103 0.456767487594567, 104 0.4558285978230622, 105 0.4549589733763721,
                 106 0.4541150119518246, 107 0.4532473368288942, 108 0.4524147996534781, 109 0.4516155756874308, 110 0.4508479688378081,
                 111 0.4501103988660299, 112 0.449441160361981, 113 0.4488991683857082, 114 0.4483790853485015, 115 0.4478798497479739,
                 116 0.4472385333536187, 117 0.4466199119869901, 118 0.4460265147880823, 119 0.4457170004412839, 120 0.4454286608950099,
                 121 0.445155988866268, 122 0.4447062610087444, 123 0.4440581628854696, 124 0.4437193152525811, 125 0.4433936089093366,
                 126 0.4430804229528626, 127 0.4427791709240014, 128 0.4424892985474526, 129 0.4422102816469686, 130 0.4419416242194622,
                 131 0.4416432968583534, 132 0.4413233479511249, 133 0.4409370501398064, 134 0.4405210674202905, 135 0.4402991813263996,
                 136 0.4401130340877754, 137 0.4398788765041312, 138 0.4396181966671472, 139 0.4393949616449583, 140 0.4392195836938776,
                 141 0.439026792099709, 142 0.4389267600053253, 143 0.4388389710138978, 144 0.4387573802492897, 145 0.4385791813462728,
                 146 0.4382898921651764, 147 0.4380765346698408, 148 0.437993268668763, 149 0.4379280714074418, 150 0.4378672055613017,
                 151 0.4378104903550605, 152 0.4377577526192519, 153 0.4377088264300963, 154 0.4376261467628988, 155 0.4374750282026258,
                 156 0.4373280488267583, 157 0.437216920897879, 158 0.4371593221303501, 159 0.4371060800942551, 160 0.4370277734992487/
** Climate damage parameters:
        a2       Quadratic multiplier (DICE 2016)                      /0.00236/
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
* nonco2eq1(tearly)..  nonco2(tearly) =E= -0.1365270772342518 + (0.0082836950889661)*EIND(tearly) + (0.010585466099088)*quantile + (0.010257028140334)*tearly.val;
* nonco2eq2(tlate)..   nonco2(tlate)  =E= -0.1365270772342518 + (0.0082836950889661)*EIND(tlate) + (0.010585466099088)*quantile + (0.010257028140334)*27;
 forceq(t)..          FORC(t)        =E= fco22x * ((log((CO2(t)/co2_1750))/log(2))) + nonco2(t);
 damfraceq(t) ..      DAMFRAC(t)     =E= a2*T1(t)**2;
 dameq(t)..           DAMAGES(t)     =E= YGROSS(t) * DAMFRAC(t);
 abateeq(t)..         ABATECOST(t)   =E= YGROSS(t) * cost1(t) * (MIU(t)**expcost2);
 mcabateeq(t)..       MCABATE(t)     =E= pbacktime(t) * MIU(t)**(expcost2-1);
 carbpriceeq(t)..     CPRICE(t)      =E= pbacktime(t) * (MIU(t))**(expcost2-1);
 etreeeq(t)..         etree(t)       =e= (1.538474426008423 + (0.0463971352999719)*EIND(t) + (-0.1893399075947444)*t.val) * (1 - 1/(1+exp(-1.00*(t.val-35))));
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
ppm(t)        = co2.l(t)/2.1290606558508802;

** CALCULATE NON-CO2 EMISSIONS
so2(tearly) = 65.8889 + 0.4514*eind.l(tearly) - 5.3944*tearly.val + 0.1335*tearly.val**2;
so2(tlate)  = 65.8889 + 0.4514*eind.l(tlate) - 5.3944*27 + 0.1335*27**2;
ch4(tearly) = 203.4439 + 4.2581*eind.l(tearly) - 5.2576*tearly.val + 0.1471*tearly.val**2;
ch4(tlate)  = 203.4439 + 4.2581*eind.l(tlate) - 5.2576*27 + 0.1471*27**2;

* Produces a file "Dice2016R-091916ap.csv" in the base directory
* For ALL relevant model outputs, see 'PutOutputAllT.gms' in the Include folder.
* The statement at the end of the *.lst file "Output..." will tell you where to find the file.

file results /"mean_config.csv"/; results.nd = 10 ; results.nw = 0 ; results.pw=20000; results.pc=5;
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
