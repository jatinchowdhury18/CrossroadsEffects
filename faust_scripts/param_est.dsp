import("stdfaust.lib");

fb2_d1ed99cf = +~(_ <: (_*0.1767554363694456, _*-0.011662407054127442) : (_, @(1)) :> _);

process = _,_ : fb2_d1ed99cf,fb2_d1ed99cf : _,_;
