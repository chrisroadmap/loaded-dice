* Base carbon price (do not optimize)
* Warning: If parameters changed, the next equation might make infeasible in base case.
* If so reduce tnopol so that don't run out of resources.
* Control variables

ifopt=0;
tatm.up(t)=15; 
*cprice.up(t)$(t.val>tnopol) = 1000;
*cprice.up(t) = cpricebase(t);

* Solve

If (ifopt eq 0,
       a2 = 0;
       solve CO2 maximizing UTILITY using nlp;
       photel(t)=cprice.l(t);
       a2 = a20;
      cprice.up(t)$(t.val<tnopol+1) = max(photel(t),cpricebase(t));
);

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

