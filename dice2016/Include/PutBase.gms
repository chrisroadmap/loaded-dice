*File I/O - Inputs Outputs


file results21 /output\GAMS_Base_1.csv/; results21.nd = 15 ; results21.nw = 0  ;put results21; results21.pc=5;
*Set
*T_OUT1(T)    a subset of T (the periods written out)     /1*10/;
$include Include\PutOutput0010.gms
putclose;

file results22 /output\GAMS_Base_2.csv/; results22.nd = 15 ; results22.nw = 0  ;put results22; results22.pc=5;
*Set
*T_OUT2(T)    a subset of T (the periods written out)     /11*20/;
$include Include\PutOutput1020.gms
putclose;

file results23 /output\GAMS_Base_3.csv/; results23.nd = 15 ; results23.nw = 0  ;put results23; results23.pc=5;
*Set
*T_OUT3(T)    a subset of T (the periods written out)     /21*30/;
$include Include\PutOutput2030.gms
putclose;

file results24 /output\GAMS_Base_4.csv/; results24.nd = 15 ; results24.nw = 0  ;put results24; results24.pc=5;
*Set
*T_OUT4(T)    a subset of T (the periods written out)     /31*40/;
$include Include\PutOutput3040.gms
putclose;

file results25 /output\GAMS_Base_5.csv/; results25.nd = 15 ; results25.nw = 0  ;put results25; results25.pc=5;
*Set
*T_OUT5(T)    a subset of T (the periods written out)     /41*50/ ;
$include Include\PutOutput4050.gms
putclose;

file results26 /output\GAMS_Base_6.csv/; results26.nd = 15 ; results26.nw = 0  ;put results26; results26.pc=5;
*Set
*T_OUT6(T)    a subset of T (the periods written out)     /51*60/  ;
$include Include\PutOutput5060.gms
putclose;