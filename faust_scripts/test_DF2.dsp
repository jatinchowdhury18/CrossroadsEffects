import("stdfaust.lib");

gain_01bc2b74 = _*-1.7990948352036202;
delay_e7964b84 = @(1);
gain_3d459ead = _*0.8175108129889816;
split_efa39fb7 = _ <: (gain_01bc2b74), (delay_e7964b84 : gain_3d459ead) :> _;

gain_063ad6f0 = _*-1.0;
fb_2888c3bc = +~(split_efa39fb7 : gain_063ad6f0);

gain_b42b42e7 = _*0.00460399444634034;
delay_b294ab50 = @(1);
gain_8ed22d04 = _*0.00920798889268068;
delay_dec20c20 = @(2);
gain_eef7cd53 = _*0.00460399444634034;
split_1edd43ea = _ <: (gain_b42b42e7), (delay_b294ab50 : gain_8ed22d04), (delay_dec20c20 : gain_eef7cd53) :> _;


process = _,_ : fb_2888c3bc,fb_2888c3bc : split_1edd43ea,split_1edd43ea : _,_;
