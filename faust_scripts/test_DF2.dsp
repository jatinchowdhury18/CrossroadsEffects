import("stdfaust.lib");

gain_4f33f314 = _*-1.7990948352036202;
delay_d37f386c = @(1);
gain_2037e6b2 = _*0.8175108129889816;
split_6eec9750 = _ <: (gain_4f33f314), (delay_d37f386c : gain_2037e6b2) :> _;

gain_25f5e2ad = _*-1.0;
fb_8a7ff103 = +~(split_6eec9750 : gain_25f5e2ad);

gain_22315d15 = _*0.00460399444634034;
delay_00a6c550 = @(1);
gain_09d58418 = _*0.00920798889268068;
delay_ed467844 = @(2);
gain_77f034b5 = _*0.00460399444634034;
split_a1d0b7f9 = _ <: (gain_22315d15), (delay_00a6c550 : gain_09d58418), (delay_ed467844 : gain_77f034b5) :> _;


process = _,_ : fb_8a7ff103,fb_8a7ff103 : split_a1d0b7f9,split_a1d0b7f9 : _,_;
