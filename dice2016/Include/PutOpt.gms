*File I/O - Inputs Outputs


file results11 /output\GAMS_Opt_1.csv/; results11.nd = 15 ; results11.nw = 0  ;put results11; results11.pc=5;
Set
T_OUT1(T)    a subset of T (the periods written out)     /1*10/;
$include Include\PutOutput0010.gms
putclose;

file results12 /output\GAMS_Opt_2.csv/; results12.nd = 15 ; results12.nw = 0  ;put results12; results12.pc=5;
Set
T_OUT2(T)    a subset of T (the periods written out)     /11*20/;
$include Include\PutOutput1020.gms
putclose;

file results13 /output\GAMS_Opt_3.csv/; results13.nd = 15 ; results13.nw = 0  ;put results13; results13.pc=5;
Set
T_OUT3(T)    a subset of T (the periods written out)     /21*30/;
$include Include\PutOutput2030.gms
putclose;

file results14 /output\GAMS_Opt_4.csv/; results14.nd = 15 ; results14.nw = 0  ;put results14; results14.pc=5;
Set
T_OUT4(T)    a subset of T (the periods written out)     /31*40/;
$include Include\PutOutput3040.gms
putclose;

file results15 /output\GAMS_Opt_5.csv/; results15.nd = 15 ; results15.nw = 0  ;put results15; results15.pc=5;
Set
T_OUT5(T)    a subset of T (the periods written out)     /41*50/ ;
$include Include\PutOutput4050.gms
putclose;

file results16 /output\GAMS_Opt_6.csv/; results16.nd = 15 ; results16.nw = 0  ;put results16; results16.pc=5;
Set
T_OUT6(T)    a subset of T (the periods written out)     /51*60/  ;
$include Include\PutOutput5060.gms
putclose;