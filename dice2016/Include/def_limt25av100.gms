
* Optimal run

ifopt=1;
avtemp200.up(t)=25; 
avtemp100.up(t)=2.5;
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

