import("stdfaust.lib");

unit_delay_b781e2f7 = @(1);
gain_bcdd61d6 = _*1.0;
split_0afcca1b = _ <: (unit_delay_b781e2f7), (gain_bcdd61d6) :> _;

unit_delay_08aaabe4 = @(1);
gain_df56d5f1 = _*1.0;
unit_delay_95a9f64c = @(1);
split_1b3af4fc = _ <: _, (gain_df56d5f1 : unit_delay_95a9f64c) :> _;

gain_1e1ae59f = _*1.0;
gain_5593d5e3 = _*1.0;
split_179bb9d1 = _ <: _, (gain_5593d5e3) :> _;

delay_8437b3b5 = @(2);
unit_delay_3e7973fc = @(1);
split_263152df = _ <: _, (unit_delay_3e7973fc) :> _;

gain_dbc941d5 = _*1.0;
split_8847f360 = _ <: _, (gain_dbc941d5) :> _;

unit_delay_db7c250c = @(1);
split_e68f5db4 = _ <: (split_0afcca1b : unit_delay_08aaabe4 : split_1b3af4fc : gain_1e1ae59f), (split_179bb9d1 : delay_8437b3b5 : split_263152df : split_8847f360 : unit_delay_db7c250c) :> _;

unit_delay_e4607853 = @(1);
gain_83f60106 = _*1.0;
split_d9f6e5c3 = _ <: (unit_delay_e4607853), (gain_83f60106) :> _;

unit_delay_b3e56e9d = @(1);
gain_a2add5b9 = _*1.0;
unit_delay_bf7270df = @(1);
split_071b8d3e = _ <: _, (gain_a2add5b9 : unit_delay_bf7270df) :> _;

gain_1acb0bec = _*1.0;
gain_19a0de10 = _*1.0;
split_847e02c8 = _ <: _, (gain_19a0de10) :> _;

unit_delay_a5fed8fa = @(1);
unit_delay_f55b28f5 = @(1);
split_b7dabbb4 = _ <: _, (unit_delay_f55b28f5) :> _;

gain_5e0880e6 = _*1.0;
split_95cd573d = _ <: _, (gain_5e0880e6) :> _;

unit_delay_31a56c6c = @(1);
split_a563e073 = _ <: (split_d9f6e5c3 : unit_delay_b3e56e9d : split_071b8d3e : gain_1acb0bec), (split_847e02c8 : unit_delay_a5fed8fa : split_b7dabbb4 : split_95cd573d : unit_delay_31a56c6c) :> _;

gain_f5373753 = _*1.0;
split_4e676f4a = _ <: _, (gain_f5373753) :> _;

unit_delay_684727da = @(1);
gain_0fea64bf = _*1.0;
unit_delay_a94ec2ae = @(1);
split_0a2b7362 = _ <: _, (gain_0fea64bf : unit_delay_a94ec2ae) :> _;

gain_010baab6 = _*1.0;
gain_aa62326f = _*1.0;
split_450f379a = _ <: _, (gain_aa62326f) :> _;

unit_delay_0c4236d1 = @(1);
unit_delay_5a3d259d = @(1);
split_5c6ca349 = _ <: _, (unit_delay_5a3d259d) :> _;

gain_c638d171 = _*1.0;
split_198bc188 = _ <: _, (gain_c638d171) :> _;

unit_delay_4e16fbe3 = @(1);
split_fe2ece51 = _ <: (split_4e676f4a : unit_delay_684727da : split_0a2b7362 : gain_010baab6), (split_450f379a : unit_delay_0c4236d1 : split_5c6ca349 : split_198bc188 : unit_delay_4e16fbe3) :> _;

gain_91fb1419 = _*1.0;
unit_delay_4005342d = @(1);
split_72080189 = _ <: _, (gain_91fb1419 : unit_delay_4005342d) :> _;

split_3b0d1c62 = _ <: (split_e68f5db4), (split_a563e073 : split_fe2ece51 : split_72080189) :> _;


process = _,_ : split_3b0d1c62,split_3b0d1c62 : _,_;
