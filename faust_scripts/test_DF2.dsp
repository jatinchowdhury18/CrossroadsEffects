import("stdfaust.lib");

gain_f588398f = _*-1.7990948352036202;
unit_delay_f56f6328 = @(1);
gain_fe7cf2de = _*0.8175108129889816;
split_403b0e22 = _ <: (gain_f588398f), (unit_delay_f56f6328 : gain_fe7cf2de) :> _;

gain_f48c8846 = _*-1.0;
fb_58a6787a = +~(split_403b0e22 : gain_f48c8846);

gain_83e62be6 = _*0.00460399444634034;
unit_delay_33586bf0 = @(1);
gain_944cc568 = _*0.00920798889268068;
unit_delay_39bbe0bf = @(1);
unit_delay_105eba9e = @(1);
gain_2f4a8028 = _*0.00460399444634034;
split_62996b8d = _ <: (gain_83e62be6), (unit_delay_33586bf0 : gain_944cc568), (unit_delay_39bbe0bf : unit_delay_105eba9e : gain_2f4a8028) :> _;


process = _,_ : fb_58a6787a,fb_58a6787a : split_62996b8d,split_62996b8d : _,_;
