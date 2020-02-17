import("stdfaust.lib");

gain_19d99738 = _*2.000090066303114;
cubic_3d3bf037 = min(1) : max(-1) : cubic with{ cubic(x) = x - x*x*x/3; };

process = _,_ : gain_19d99738,gain_19d99738 : cubic_3d3bf037,cubic_3d3bf037 : _,_;
