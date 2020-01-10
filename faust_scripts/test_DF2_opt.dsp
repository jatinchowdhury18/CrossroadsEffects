import("stdfaust.lib");

gain_3f894f1e = _*-1.4320450453708604;
delay_96921c37 = @(1.0);
gain_54540ac1 = _*0.5594923063264857;
split_d072f08a = _ <: (gain_3f894f1e), (delay_96921c37 : gain_54540ac1) :> _;

gain_eaf05bcf = _*-0.8947764712702115;
fb_f77c307a = +~(split_d072f08a : gain_eaf05bcf);

gain_f01b7d64 = _*0.049408296898725446;
delay_ec340a6f = @(1.0);
gain_35431914 = _*-0.09313011490341294;
delay_7b86b1d4 = @(2.0);
gain_83fb850e = _*0.07047714013418019;
split_8bfbe1a0 = _ <: (gain_f01b7d64), (delay_ec340a6f : gain_35431914), (delay_7b86b1d4 : gain_83fb850e) :> _;


process = _,_ : fb_f77c307a,fb_f77c307a : split_8bfbe1a0,split_8bfbe1a0 : _,_;
