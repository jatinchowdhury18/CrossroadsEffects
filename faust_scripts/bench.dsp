import("stdfaust.lib");

gain_245d0569 = _*1.0;
gain_9ddb8d34 = _*1.0;
gain_c6de63ef = _*1.0;
gain_644c5c76 = _*1.0;
split_14540055 = _ <: (gain_245d0569 : gain_9ddb8d34), (gain_c6de63ef), (gain_644c5c76) :> _;


process = _,_ : split_14540055,split_14540055 : _,_;
