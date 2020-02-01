import("stdfaust.lib");

gain_82dde674 = _*0.3001620345811654;
unit_delay_df254f42 = @(1);
gain_5c10c3f9 = _*-0.4003134948531553;
unit_delay_41ee44a5 = @(1);
unit_delay_58bfb456 = @(1);
gain_b004b90c = _*0.12039620102929133;
unit_delay_7a643a1d = @(1);
unit_delay_a590f107 = @(1);
unit_delay_f054c249 = @(1);
gain_66c7a0f9 = _*0.19961285211481916;
unit_delay_38c9c9fb = @(1);
unit_delay_879b5d1f = @(1);
unit_delay_f5f30cc2 = @(1);
unit_delay_c5778a36 = @(1);
gain_084ac5e7 = _*-0.7500201657152571;
split_19c13a67 = _ <: (gain_82dde674), (unit_delay_df254f42 : gain_5c10c3f9), (unit_delay_41ee44a5 : unit_delay_58bfb456 : gain_b004b90c), (unit_delay_7a643a1d : unit_delay_a590f107 : unit_delay_f054c249 : gain_66c7a0f9), (unit_delay_38c9c9fb : unit_delay_879b5d1f : unit_delay_f5f30cc2 : unit_delay_c5778a36 : gain_084ac5e7) :> _;


process = _,_ : split_19c13a67,split_19c13a67 : _,_;
