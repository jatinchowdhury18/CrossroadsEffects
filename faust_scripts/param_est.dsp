import("stdfaust.lib");

delay_4d136109 = @(85);
gain_ea54b4b9 = _*-0.3735337504293355;
split_19606e72 = _ <: _, (delay_4d136109 : gain_ea54b4b9) :> _;

gain_17566532 = _*0.3030461456460897;

process = _,_ : split_19606e72,split_19606e72 : gain_17566532,gain_17566532 : _,_;
