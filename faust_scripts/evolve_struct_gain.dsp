import("stdfaust.lib");

gain_5647be6d = _*-0.10000038515678848;
gain_e9f6afa3 = _*-0.10000038515678848;
split_763e49f1 = _ <: (gain_5647be6d), (gain_e9f6afa3) :> _;


process = _,_ : split_763e49f1,split_763e49f1 : _,_;
