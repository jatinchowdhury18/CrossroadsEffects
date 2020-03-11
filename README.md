# Crossroads Effects

[![Build Status](https://travis-ci.com/jatinchowdhury18/CrossroadsEffects.svg?token=Ub9niJrqG1Br1qaaxp7E&branch=master)](https://travis-ci.com/jatinchowdhury18/CrossroadsEffects)

This repository contains a system (still in developement)
for auto-generating audio effects for a given input and
output audio file. More technically, the system uses a `Python`
script to generate `Faust` code that compiles to create audio
effects. The `Faust` code is then optimized to create an effect
that best approximates the desired output, using a variety of
optimization schemes as well as genetic algorithms.

## Using

This project is still in the early stages of development.
To test that the system is working on your machine, run
`run_tests.sh --quick`.

### Dependencies

To use `Crossroads`, you must have the following dependencies
installed:

- [`Python`](https://www.python.org/)
- `Python` packages (`pip install -r requirements.txt`)
- [`Faust`](https://github.com/grame-cncm/faust)
- Mac/Linux only
  - Boost (`sudo apt-get install libboost-all-dev`)
  - libsndfile (optional, see [below](#using-with-libsndfile))
- Windows only
  - [MSYS2](https://www.msys2.org/)

If you don't already have `Faust` installed, it is included in 
this repo and can be installed as follows (this requires CMAKE):

```bash
# Starting from the root directory of this repo
cd modules/Faust
make
sudo make install
```

### Installation
```bash
# clone repo
git clone https://github.com/jatinchowdhury18/CrossroadsEffects.git
cd CrossroadsEffects

# initialize submodules
git submodule update --init --recursive

# If you don't already have Faust installed (requires cmake)
cd modules/Faust/
make
sudo make install
cd ../../

# Run tests (this will take a few minutes)
./run_tests.sh --quick
```

### Running

To use Crossroads, you must have an input audio file, and a
desired output audio file. Crossroads will attempt to generate
an audio effect that can create the desired output from the given
input. As an example, the `audio_files/` directory contains
a drum sample (`drums.wav`), and the same sample with a lower
volume (`gain.wav`).

```bash
# Run `python crossroads.py --name=<EffectName> <input file> <desired output file>`
# (this will take a couple hours)
python crossroads.py --name=MyGain audio_files/drums.wav audio_files/gain.wav
```
Crossroads will generate a folder called `MyGain` that contains
`Faust` code, VST plugins, and SVG block diagrams generated by 
Crossroads.

### Using with libsndfile

Installing [`libsndfile`](https://github.com/erikd/libsndfile) is
not strictly necessary, but can improve the speed of the algorithm
by 2x or more. To install use 
`sudo apt-get install  libsndfile-dev` (Linux), or
`brew install libsndfile` (Mac).

If you don't want to use `libsndfile`, navigate to
`crossroads_scripts/param_estimation.py` and set the flag
`USING_LIBSNDFILE=False` on line 10.

## How It Works

Crossroads uses a genetic algorithm to generate signal processing
structures, made up of gain and delay elements. A gradient-based
optimizer (L-BFGS-B) is then used to tune the parameters of each 
structure. Crossroads generates `Faust` code for each structure,
then compiles a VST plugin, and runs the input audio through the
plugin. The output audio is then compared to the desired audio
using a combination of time-domain and frequency-domain error
functions. Finally, the results of the error functions are fed
back to the genetic algorithm which generates a new generation
of structures.

For example, let's say we have an effect that we want to clone.
Unbeknownst to us, the effect simply performs a 2-sample feed-forward
comb filter. We can choose an input audio file, process it through the
effect, then submit both audio files to Crossroads. Crossroads will
then be able to evolve the cloned structure as follows:

<img src=https://ccrma.stanford.edu/~jatin/comb_evolve.gif width=66%>

### Current Status and Future Work

Currently Crossroads is only configured to generate
feedforward systems. The foundations exist to generate systems
that contain feedback, but implementing the parameter estimation 
step for systems with complex poles is still in progress.

## About the name

In German legend, a character named Faust makes a deal with
the devil, to give up his soul for unlimited knowledge and all
the pleasures he can imagine. In Blues legend, Robert Johnson 
makes a deal with the devil to become the greatest Blues guitarist
of all time, in exchange for his soul. In audio programming, 
signal processing engineers are making a deal with the devil to
give up creating their own DSP algorithms in exchange for machine
learning algorithms that accomplish these signal processing tasks
for them. In each case, the deal with the devil always takes place
at a crossroads . . .

## Contributing

Contributions are most welcome! In particular adding new base
elements (see `crossroads_scripts/gen_faust.py`), or adding new
evolutionary strategies (`crossroads_scripts/evolve_structure.py`).
Feel free to contact us with any questions!

## License

The code in this repository is licensed under the GNU Lesser General
Public License. Note that any code generated by this system is **not**
covered under this license, and can be licensed independently.
