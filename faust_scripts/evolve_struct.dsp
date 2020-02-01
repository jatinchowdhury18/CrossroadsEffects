import("stdfaust.lib");

gain_6b54cc4f = _*-0.20000485467822135;

process = _,_ : gain_6b54cc4f,gain_6b54cc4f : _,_;
