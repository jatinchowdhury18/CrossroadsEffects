import("stdfaust.lib");

delay_0791a1d0 = @(91);
gain_5081fe06 = _*-0.198134006696245;
split_c4097f96 = _ <: _, (delay_0791a1d0 : gain_5081fe06) :> _;

gain_c3538fe1 = _*0.3084216750061773;

process = _,_ : split_c4097f96,split_c4097f96 : gain_c3538fe1,gain_c3538fe1 : _,_;
