* Reset parameters
AA1 = 0;
AA2 = 0;

*No control rate, no limits on cprice.
miu.lo(t)=.000;
cprice.up(T) = 999  ;
cprice.lo(T) = .000 ;

*Solve new model
solve CO2 maximizing UTILITY using nlp ;
*solve CO2 maximizing UTILITY using nlp ;
*solve CO2 maximizing UTILITY using nlp ;


* Definition of hotelling results
miuhotel(t) = miu.l(t);
hotel_SCC(T) = -1000*eeq.m(t)/yy.m(t);
