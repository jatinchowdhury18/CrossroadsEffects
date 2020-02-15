import("stdfaust.lib");

gain_748411aa = _*0.29876635941400853;
gain_3b4f1a56 = _*0.53194650732673;
unit_delay_f6160843 = @(1);
gain_689ee769 = _*-0.15398358194380563;
split_6fd10691 = _ <: (gain_3b4f1a56), (unit_delay_f6160843 : gain_689ee769) :> _;

unit_delay_40ebdc09 = @(1);
gain_c1e556ec = _*-0.9893130293690344;
gain_2927421e = _*0.7561344529535868;
unit_delay_eecae516 = @(1);
gain_f4768e27 = _*0.09671978613651143;
split_5aa958d8 = _ <: (gain_2927421e), (unit_delay_eecae516 : gain_f4768e27) :> _;

split_8cdd354e = _ <: (gain_748411aa), (split_6fd10691 : unit_delay_40ebdc09 : gain_c1e556ec : split_5aa958d8) :> _;

unit_delay_d61e1cc1 = @(1);
gain_ccbc0dc1 = _*-0.27108882748998064;
unit_delay_0907ff9c = @(1);
gain_071e4516 = _*-1.4731654820527655;
split_f9425cb1 = _ <: (gain_ccbc0dc1), (unit_delay_0907ff9c : gain_071e4516) :> _;

gain_2ffdbf7c = _*0.0028950285670715633;
gain_32604f2f = _*-0.35254022444931177;
unit_delay_0f1e1856 = @(1);
gain_7685a561 = _*0.817003440047692;
split_8bac1771 = _ <: (gain_32604f2f), (unit_delay_0f1e1856 : gain_7685a561) :> _;

unit_delay_274e99cc = @(1);
gain_cc28dd5f = _*0.6233495494040621;
split_28397796 = _ <: (gain_2ffdbf7c), (split_8bac1771 : unit_delay_274e99cc : gain_cc28dd5f) :> _;

split_afc44ee0 = _ <: (split_8cdd354e), (unit_delay_d61e1cc1 : split_f9425cb1 : split_28397796) :> _;


process = _,_ : split_afc44ee0,split_afc44ee0 : _,_;
