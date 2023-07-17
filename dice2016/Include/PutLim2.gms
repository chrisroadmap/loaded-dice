*File I/O - Inputs Outputs


file results31 /output\GAMS_Lim2_1.csv/; results31.nd = 15 ; results31.nw = 0  ;put results31; results31.pc=5;
*Set
*T_OUT1(T)    a subset of T (the periods written out)     /1*10/;
$include Include\PutOutput0010.gms
putclose;

file results32 /output\GAMS_Lim2_2.csv/; results32.nd = 15 ; results32.nw = 0  ;put results32; results32.pc=5;
*Set
*T_OUT2(T)    a subset of T (the periods written out)     /11*20/;
$include Include\PutOutput1020.gms
putclose;

file results33 /output\GAMS_Lim2_3.csv/; results33.nd = 15 ; results33.nw = 0  ;put results33; results33.pc=5;
*Set
*T_OUT3(T)    a subset of T (the periods written out)     /21*30/;
$include Include\PutOutput2030.gms
putclose;

file results34 /output\GAMS_Lim2_4.csv/; results34.nd = 15 ; results34.nw = 0  ;put results34; results34.pc=5;
*Set
*T_OUT4(T)    a subset of T (the periods written out)     /31*40/;
$include Include\PutOutput3040.gms
putclose;

file results35 /output\GAMS_Lim2_5.csv/; results35.nd = 15 ; results35.nw = 0  ;put results35; results35.pc=5;
*Set
*T_OUT5(T)    a subset of T (the periods written out)     /41*50/ ;
$include Include\PutOutput4050.gms
putclose;

file results36 /output\GAMS_Lim2_6.csv/; results36.nd = 15 ; results36.nw = 0  ;put results36; results36.pc=5;
*Set
*T_OUT6(T)    a subset of T (the periods written out)     /51*60/  ;
$include Include\PutOutput5060.gms
putclose;