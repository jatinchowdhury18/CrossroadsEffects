import("stdfaust.lib");

gain_c3c4d4e1 = _*-0.19996961967694077;
fb_64746921 = +~(gain_c3c4d4e1);


process = _,_ : fb_64746921,fb_64746921 : _,_;
