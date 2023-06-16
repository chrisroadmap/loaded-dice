* Discount program

ifopt=1;
elasmu   = .001;
prstp    = .01;
rr(t) = 1/((1+prstp)**(tstep*(t.val-1)));
optlrsav = (dk + .004)/(dk + .004*elasmu + prstp)*gama;
k0 = 410;
k.FX(tfirst)      = k0;
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

ifopt=1;

prstp    = .01;
rr(t) = 1/((1+prstp)**(tstep*(t.val-1)));
optlrsav = (dk + .004)/(dk + .004*elasmu + prstp)*gama;
