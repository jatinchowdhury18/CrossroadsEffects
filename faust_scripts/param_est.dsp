import("stdfaust.lib");

fb2_fb253bbd = +~(_ <: (_*-0.9948322975615345, _*0.2499137372881346) : (_, @(1)) :> _);
gain_dda37b3e = _*0.9999949300608746;
unit_delay_2712f96e = @(1);
gain_78cb2161 = _*1.0;
unit_delay_b81b9b5e = @(1);
unit_delay_5f39c7fd = @(1);
gain_489b2b73 = _*0.9999949300608746;
split_f15b8e47 = _ <: (gain_dda37b3e), (unit_delay_2712f96e : gain_78cb2161), (unit_delay_b81b9b5e : unit_delay_5f39c7fd : gain_489b2b73) :> _;


process = _,_ : fb2_fb253bbd,fb2_fb253bbd : split_f15b8e47,split_f15b8e47 : _,_;
