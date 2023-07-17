* Solve equations for optimal case

ifopt=1;

* Solve
solve CO2 maximizing UTILITY using nlp ;
solve CO2 maximizing UTILITY using nlp ;
solve CO2 maximizing UTILITY using nlp ;

*Post-Solution Parameter-Assignment

scc(t) = -1000*eco2eq.m(t)/(.00001+cc.m(t));
ppm(t)    = mat.l(t)/2.13;
abaterat(t) = abatecost.l(t)/y.l(t);
atfrac2020(t) = ((mat.l(t)-mat0)/(ccatot.l(t)+.00001-CumEmiss0  ));
atfrac1765(t) = ((mat.l(t)-mateq)/(.00001+ccatot.l(t)  ));
FORC_CO2(t) = fco22x*((log((MAT.l(t)/mateq))/log(2))); 