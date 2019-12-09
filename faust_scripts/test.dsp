import("stdfaust.lib");
drive = hslider("Drive",1.0,0.0,1.0,0.01) : si.smoo;
process = ef.ef.cubicnl(drive, 0);
