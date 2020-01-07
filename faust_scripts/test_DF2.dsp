import("stdfaust.lib");

gain_baa19bd4 = _*-1.7990948352036202;
delay_9c623384 = @(1);
gain_43b91175 = _*0.8175108129889816;
split_fc8e4b5a = _ <: (gain_baa19bd4), (delay_9c623384 : gain_43b91175) :> _;

gain_30a4e7b4 = _*-1.0;
fb_c16058f0 = +~(split_fc8e4b5a : gain_30a4e7b4);

gain_85f5cae6 = _*0.00460399444634034;
delay_570b46f6 = @(1);
gain_50ec5ca2 = _*0.00920798889268068;
delay_755a39e1 = @(2);
gain_53661391 = _*0.00460399444634034;
split_e8d4fbcd = _ <: (gain_85f5cae6), (delay_570b46f6 : gain_50ec5ca2), (delay_755a39e1 : gain_53661391) :> _;


process = _,_ : fb_c16058f0,fb_c16058f0 : split_e8d4fbcd,split_e8d4fbcd : _,_;
