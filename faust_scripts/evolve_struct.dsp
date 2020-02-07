import("stdfaust.lib");

gain_05042712 = _*0.13865438718714387;
gain_28461af3 = _*1.0194167558962126;
split_ceb25998 = _ <: _, (gain_28461af3) :> _;


process = _,_ : gain_05042712,gain_05042712 : split_ceb25998,split_ceb25998 : _,_;
