import("stdfaust.lib");

gain_b57ed9d4 = _*1.999997573265699;
cubic_5e4a807e = min(1) : max(-1) : cubic with{ cubic(x) = x - x*x*x/3; };
unit_delay_055b2ec0 = @(1);
gain_8f965464 = _*-2.1952812579798725e-05;
split_2a8b6c89 = _ <: (gain_b57ed9d4 : cubic_5e4a807e), (unit_delay_055b2ec0 : gain_8f965464) :> _;


process = _,_ : split_2a8b6c89,split_2a8b6c89 : _,_;
