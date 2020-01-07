import("stdfaust.lib");

delay_f234e63a = _';
gain_3c0e764e = _*0.5;
delay_0b05e240 = _';
gain_d1abd39a = _*0.8;
split_d5f064ea = _ <: (gain_3c0e764e), (delay_0b05e240 : gain_d1abd39a) :> _;

fb_f0c66601 = +~(delay_f234e63a : split_d5f064ea);

gain_0868b5aa = _*0.2;
delay_fa63c36b = _';
gain_df970ff1 = _*0.2;
delay_9500aa2f = _';
gain_ea17b6c2 = _*-0.1;
split_ed9cb69a = _ <: (gain_df970ff1), (delay_9500aa2f : gain_ea17b6c2) :> _;

split_67abff37 = _ <: (gain_0868b5aa), (delay_fa63c36b : split_ed9cb69a) :> _;


process = _ : fb_f0c66601 : split_67abff37 : _;
