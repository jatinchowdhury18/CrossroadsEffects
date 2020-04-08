import("stdfaust.lib");

gain_2cbe42d4 = _*-1.7990948352036202;
unit_delay_b85c90ad = @(1);
gain_098d27bb = _*0.8175108129889816;
split_8161512f = _ <: (gain_2cbe42d4), (unit_delay_b85c90ad : gain_098d27bb) :> _;

gain_c74af7a2 = _*-1.0;
fb_1946e1f2 = +~(split_8161512f : gain_c74af7a2);

gain_4f598442 = _*0.00460399444634034;
unit_delay_4f055429 = @(1);
gain_c7fccf65 = _*0.00920798889268068;
unit_delay_a10b18e0 = @(1);
unit_delay_9a6e0143 = @(1);
gain_c49491e4 = _*0.00460399444634034;
split_ff31980b = _ <: (gain_4f598442), (unit_delay_4f055429 : gain_c7fccf65), (unit_delay_a10b18e0 : unit_delay_9a6e0143 : gain_c49491e4) :> _;


process = _,_ : fb_1946e1f2,fb_1946e1f2 : split_ff31980b,split_ff31980b : _,_;
