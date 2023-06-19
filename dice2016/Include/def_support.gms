
* Optimal run

ifopt=1  ;

miu.up(t)$(t.val<tswitch) =.2*(1+deltamiu)**(5*(t.val-1));
miu.up(t)$(t.val>tswitch-1) =1.2;
abaterat.up(t)=abateratmax;


* Solve
solve CO2 maximizing UTILITY using nlp ;
solve CO2 maximizing UTILITY using nlp ;
solve CO2 maximizing UTILITY using nlp ;

*Post-Equation Parameter-Assignment
*to 'save' variables under multiple runs, we need to declare them in advance and fix them before executing another 'solve' command.
* Calculate social cost of carbon and other variables

scc(t) = -1000*eeq.m(t)/(.00001+cc.m(t));
atfrac(t) = ((mat.l(t)-588)/(ccatot.l(t)+.000001  ));
atfrac2010(t) = ((mat.l(t)-mat0)/(.00001+ccatot.l(t)-ccatot.l('1')  ));
ppm(t)    = mat.l(t)/2.13;

