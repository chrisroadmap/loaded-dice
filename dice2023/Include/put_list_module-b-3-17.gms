* Produces a file "DICE2022A-base-3-17-3.csv" in the base directory


put /"This is optimal if ifopt = 1 and baseline if ifopt = 0";
put /"ifopt =" ifopt;
put // "Period";
Loop (T, put T.val);
put / "Year" ;
Loop (T, put (2015+(TSTEP*T.val) ));
put / "Objective function (2019$)" ;
put utility.l;
put / "Industrial CO2 GtCO2/yr" ;
Loop (T, put EIND.l(T));
put / "Atmospheric concentration C (ppm)" ;
Loop (T, put (MAT.l(T)/2.13));
put / "Atmospheric concentrations GtC" ;
Loop (T, put mat.l(t));
put / "Atmospheric temperaturer (deg c above preind) " ;
Loop (T, put TATM.l(T));
put / "Total forcings w/m2" ;
Loop (T, put forc.l(t));
put / "Forcings, exogenous w/m2" ;
Loop (T, put F_Misc(t) );
put / "CO2 forcings w/m2" ;
Loop (T, put FORC_CO2(t) );
put / "Actual other abatable GHG forcings w/m2" ;
Loop (T, put F_GHGabate.L(t) );

put / "Carbon price (2019 $ per t CO2)" ;
Loop (T, put cprice.l(T));
put / "Emissions control rate" ;
Loop (T, put MIU.l(T));
put / "Social cost of carbon $/tCO2" ;
scc('1')=scc('2')*.85;
Loop (T, put scc(T));


put / "Output, net net trill 2019$" ;
Loop (T, put Y.l(T));
put / "Interest rate, %/yr" ;
Loop (T, put RI.l(T));
put / "Population" ;
Loop (T, put L(T));
put / "TFP" ;
Loop (T, put AL(T));
put / "Output, gross-gross, 2019$" ;
Loop (T, put YGROSS.L(t));
put / "Change TFP, %/year" ;
Loop (T, put ga(t));
put / "Capital stock, 2019$" ;
Loop (T, put k.l(t));
 put / "Savings rate, fraction gross output" ;
Loop (T, put s.l(t));
  put / "Gross investment, 2019$" ;
Loop (T, put I.l(t));
   put / "Y gross-net, 2019$" ;
Loop (T, put ynet.l(t));
put / "Consumption per capita, 2019$ " ;
Loop (T, put CPC.l(T));
put / "Consumption" ;
Loop (T, put C.l(t));



put / "Climate damages, fraction of output" ;
Loop (T, put DAMFRAC.l(T));
put / "Damages, 2019$" ;
Loop (T, put damages.l(t));

put / "Abatement, 2019$" ;
Loop (T, put abatecost.l(t));
put / "Abatement/0utput" ;
Loop (T, put  abaterat(t) );

put / "Sigmabase (CO2/output, no controls, industrial CO2)" ;
Loop (T, put sigma(t));
put / "Sigmatot,(CO2/output, no controls, all CO2)" ;
Loop (T, put sigmaTOT(t));
put / "Cost, backstop technology ($/tCO2)" ;
Loop (T, put pbacktime(T));

put / "Total CO2 Emissions, GTCO2/year" ;
Loop (T, put Eco2.l(T));
put / "Total CO2e Emissions, GTCO2-E/year" ;
Loop (T, put Eco2e.l(T));
put / "Industrial CO2 Emissions, GTCO2/year" ;
Loop (T, put EIND.l(T));
put / "Base abateable non-CO2 emission, GTCO2-E/year" ;
Loop (T, put CO2E_GHGabateB(t));
put / "Land emissions, GtCO2/year" ;
Loop (T, put eland(t));
put / "Cumulative CO2 emissions, GtC " ;
Loop (T, put ccatot.l(t));
put / "Atmospheric fraction CO2 since 1765 " ;
Loop (T, put  atfrac1765(t) );
put / "Atmospheric fraction CO2 since 2020 " ;
Loop (T, put  atfrac2020(t) );


put / "Permanent C box"
Loop (T, put res0.L(t) );
put / "Slow C box"
Loop (T, put res1.L(t)   );
put / "Medium C box"
Loop (T, put res2.L(t)  );
put / "Fast C box"
Loop (T, put res3.L(t) );
put / "Temp Box 1"
Loop (T, put TBOX1.L(t) );
put / "Temp Box 2"
Loop (T, put TBOX2.L(t) );

put / "Alpha"
Loop (T, put alpha.L(t)  );
put / "IFR"
Loop (T, put irft.L(t) );
put / "cacc"
Loop (T, put cacc.L(t) );
put / "ccatot"
Loop (T, put ccatot.L(t) );
put / "Share of output net zero emissions"
Loop (T, put cost1tot(t) );



put /"  yr0     ="      yr0     ; put " emshare0        ="      emshare0        ;put "  emshare1        ="      emshare1        ; put " emshare2        ="      emshare2        ;

put "   emshare3        ="      emshare3        ;
put "   tau0    ="      tau0    ;
put "   tau1    ="      tau1    ;
put "   tau2    ="      tau2    ;
put "   tau3    ="      tau3    ;
put "   teq1    ="      teq1    ;
put "   teq2    ="      teq2    ;
put "   d1      ="      d1      ;
put "   d2      ="      d2      ;
put "IRF0       ="      irf0;
put "   irC     ="      irC     ;
put "   irT     ="      irT     ;
put /"  fco22x  ="      fco22x  ;
put "   mat0    ="      mat0    ;
put "   res00   ="      res00   ;
put "   res10   ="      res10   ;
put "   res20   ="      res20   ;
put "   res30   ="      res30   ;
put "   mateq   ="      mateq   ;
put "   tbox10  ="      tbox10  ;
put "   tbox20  ="      tbox20  ;
put "   tatm0   ="      tatm0   ;

put /"  a2      ="      a2      ;

put "   elasmu  ="      elasmu  ;
put "   prstp   ="      prstp   ;
put "gsigma1            ="      gsigma1         ;
put "    e0     ="        e0    ;
put "expcost2           ="       expcost2       ;
put "   gback   ="       gback  ;
put "   limmiu2050      ="       limmiu2070     ;
put "   limmiu2100      ="      limmiu2120      ;
put "   cprice0         ="       cprice0        ;
put "   gcprice         ="   gcprice  ;
put /;
