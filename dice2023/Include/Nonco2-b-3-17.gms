* nonco2 Parameters      
Parameters
        CO2E_GHGabateB(t)         Abateable non-CO2 GHG emissions base
        CO2E_GHGabateact(t)       Abateable non-CO2 GHG emissions base (actual)
        F_Misc(t)                 Non-abateable forcings (GHG and other)
        emissrat(t)               Ratio of CO2e to industrial emissions
        sigmatot(t)               Emissions output ratio for CO2e       
        FORC_CO2(t)               CO2 Forcings
;      
** Parameters for non-industrial emission
** Assumes abateable share of non-CO2 GHG is 65%
Parameters
        eland0         Carbon emissions from land 2015 (GtCO2 per year)  / 5.9    /
        deland         Decline rate of land emissions (per period)       / .1     /      
        F_Misc2020     Non-abatable forcings 2020                       /  -0.054    /
        F_Misc2100     Non-abatable forcings 2100                        / .265/       
        F_GHGabate2020 Forcings of abatable nonCO2 GHG                   / 0.518 /
        F_GHGabate2100 Forcings of abatable nonCO2 GHG                   / 0.957 /

        ECO2eGHGB2020  Emis of abatable nonCO2 GHG GtCO2e  2020             /  9.96/     
        ECO2eGHGB2100  Emis of abatable nonCO2 GHG GtCO2e  2100             /  15.5 /     
        emissrat2020   Ratio of CO2e to industrial CO2 2020                 / 1.40 /
        emissrat2100   Ratio of CO2e to industrial CO2 2020                 / 1.21 /       
        Fcoef1         Coefficient of nonco2 abateable emissions            /0.00955/
        Fcoef2         Coefficient of nonco2 abateable emissions            /.861/
        ;
** Parameters emissions and non-CO2 
        eland(t) = eland0*(1-deland)**(t.val-1); eland(t) = eland0*(1-deland)**(t.val-1);       
        CO2E_GHGabateB(t)=ECO2eGHGB2020+((ECO2eGHGB2100-ECO2eGHGB2020)/16)*(t.val-1)$(t.val le 16)+((ECO2eGHGB2100-ECO2eGHGB2020))$(t.val ge 17);
        F_Misc(t)=F_Misc2020 +((F_Misc2100-F_Misc2020)/16)*(t.val-1)$(t.val le 16)+((F_Misc2100-F_Misc2020))$(t.val ge 17);
        emissrat(t) = emissrat2020 +((emissrat2100-emissrat2020)/16)*(t.val-1)$(t.val le 16)+((emissrat2100-emissrat2020))$(t.val ge 17); 
        sigmatot(t) = sigma(t)*emissrat(t);
        cost1tot(t) = pbacktime(T)*sigmatot(T)/expcost2/1000;
VARIABLES
        ECO2(t)         Total CO2 emissions (GtCO2 per year)
        ECO2E(t)        Total CO2e emissions including abateable nonCO2 GHG (GtCO2 per year)
        EIND(t)         Industrial CO2 emissions (GtCO2 per yr)
        F_GHGabate      Forcings abateable nonCO2 GHG     
;
Equations
        ECO2eq(t)         CO2 Emissions equation
        ECO2Eeq(t)        CO2E Emissions equation
        EINDeq(t)        Industrial CO2 equation
        F_GHGabateEQ(t)
;        