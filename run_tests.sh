#!/bin/sh

PY=python
if [[ "$OSTYPE" == "darwin"* || $MACHTYPE == "x86_64-redhat-linux-gnu" ]]; then
    PY=python3
fi

pattern=test_scripts/*_test_*.py
if [[ $1 == "--quick" ]]; then
    pattern=test_scripts/q_test_*.py
elif [[ $1 == "--evolve" ]]; then
    pattern=test_scripts/e_test_*.py
elif [[ $1 == "--params" ]]; then
    pattern=test_scripts/p_test_*.py
fi

if [ -z "$1" ]; then
    # test full system
    echo "Testing Crossroads"
    $PY crossroads.py --name=Gain audio_files/drums.wav audio_files/gain.wav

    echo "Checking artifacts..."
    name=Gain
    [ -d $name ] || { echo "Error: Output folder not found!" && exit 1; }
    [ -d $name/gen0_0 -a -d $name/gen0_1 -a -d $name/gen0_2 ] || { echo "Error: Generation output folders not found!" && exit 1; }
    [ -d $name/gen_final ] || { echo "Error: Final output folder not found!" && exit 1; }

    tfile=$name/gen_final/$name
    [ -e $tfile.dsp ] || { echo "Error: Output Faust script file not found!" && exit 1; }
    [ -e $tfile.dll -o -e $tfile.vst -o -e $tfile.so ] || { echo "Error: Output VST file not found!" && exit 1; }
    [ -e $name/gen_final/svgs/process.svg ] || { echo "Error: Output SVG not found" && exit 1; }
    echo "SUCCESS"
else
    # run test scripts
    for f in $pattern
    do

        echo "Running $f ..."
        $PY $f || exit 1
    done
fi
