import("stdfaust.lib");

gain_edf30b23 = _*-1.7990948352036202;
unit_delay_f41499a9 = @(1);
gain_588bd9cf = _*0.8175108129889816;
split_1c93ae41 = _ <: (gain_edf30b23), (unit_delay_f41499a9 : gain_588bd9cf) :> _;

gain_3577da2c = _*-1.0;
fb_d33cbe73 = +~(split_1c93ae41 : gain_3577da2c);

gain_8fcef107 = _*0.00460399444634034;
unit_delay_260fa293 = @(1);
gain_fd8792a1 = _*0.00920798889268068;
unit_delay_3b774b6c = @(1);
gain_39b5f0d9 = _*0.00460399444634034;
split_aafe91e9 = _ <: (gain_8fcef107), (unit_delay_260fa293 : gain_fd8792a1), (unit_delay_3b774b6c : gain_39b5f0d9) :> _;


process = _,_ : fb_d33cbe73,fb_d33cbe73 : split_aafe91e9,split_aafe91e9 : _,_;
