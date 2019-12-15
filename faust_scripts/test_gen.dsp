import("stdfaust.lib");

gain_2ca1 = _*0.5;
delay_77ec = _';
fb_9115 = +~(gain_2ca1 : delay_77ec);

process = _ : fb_9115 :  _;
