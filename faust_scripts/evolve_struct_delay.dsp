import("stdfaust.lib");

gain_03cccd32 = _*0.5000123453946032;
delay_47acd278 = @(2);
gain_294a2b09 = _*-0.2499963084025012;
split_3a936584 = _ <: (gain_03cccd32), (delay_47acd278 : gain_294a2b09) :> _;


process = _,_ : split_3a936584,split_3a936584 : _,_;
