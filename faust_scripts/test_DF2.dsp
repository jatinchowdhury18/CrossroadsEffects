import("stdfaust.lib");

gain_af1c7fec = _*-1.7990948352036202;
delay_9ecd612e = @(1);
gain_cc3de264 = _*0.8175108129889816;
split_b45e4639 = _ <: (gain_af1c7fec), (delay_9ecd612e : gain_cc3de264) :> _;

gain_e5220b91 = _*-1.0;
fb_161536cc = +~(split_b45e4639 : gain_e5220b91);

gain_c9a9650d = _*0.00460399444634034;
delay_4767e91a = @(1);
gain_d38ca928 = _*0.00920798889268068;
delay_eef49bca = @(2);
gain_832ed10f = _*0.00460399444634034;
split_318a532c = _ <: (gain_c9a9650d), (delay_4767e91a : gain_d38ca928), (delay_eef49bca : gain_832ed10f) :> _;


process = _,_ : fb_161536cc,fb_161536cc : split_318a532c,split_318a532c : _,_;
