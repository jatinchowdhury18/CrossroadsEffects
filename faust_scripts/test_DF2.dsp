import("stdfaust.lib");

gain_f6e6c91c = _*-1.7990948352036202;
delay_66c79b84 = @(1);
gain_520db630 = _*0.8175108129889816;
split_1a8b27cc = _ <: (gain_f6e6c91c), (delay_66c79b84 : gain_520db630) :> _;

gain_fd40ede1 = _*-1.0;
fb_81497343 = +~(split_1a8b27cc : gain_fd40ede1);

gain_dcef4d50 = _*0.00460399444634034;
delay_54542f94 = @(1);
gain_b11a4cd9 = _*0.00920798889268068;
delay_a3e0cbee = @(2);
gain_02ab4ec4 = _*0.00460399444634034;
split_c689b196 = _ <: (gain_dcef4d50), (delay_54542f94 : gain_b11a4cd9), (delay_a3e0cbee : gain_02ab4ec4) :> _;


process = _,_ : fb_81497343,fb_81497343 : split_c689b196,split_c689b196 : _,_;
