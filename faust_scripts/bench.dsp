import("stdfaust.lib");

gain_91797324 = _*1.0;
gain_468d866a = _*1.0;
unit_delay_c988eb83 = @(1);
gain_c3e00ad4 = _*1.0;
gain_469be2d7 = _*0.2;
split_be6e3e92 = _ <: (gain_91797324 : gain_468d866a), (unit_delay_c988eb83 : gain_c3e00ad4), (gain_469be2d7) :> _;


process = _,_ : split_be6e3e92,split_be6e3e92 : _,_;
