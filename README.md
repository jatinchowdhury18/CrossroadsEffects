# Crossroads Effects

[![Build Status](https://travis-ci.com/jatinchowdhury18/CrossroadsEffects.svg?token=Ub9niJrqG1Br1qaaxp7E&branch=master)](https://travis-ci.com/jatinchowdhury18/CrossroadsEffects)

This repository contains a system (still in developement)
for auto-generating audio effects for a given input and
output audio file. More technically, the system uses a `Python`
script to generate `Faust` code that compiles to create audio
effects. The `Faust` code is then optimized to create an effect
that best approximates the desired output, using a variety of
optimiztion schemes as well as genetic algorithms.

## Using

This project is still in the early stages of development.
To test that the system is working on your machine, run
`run_tests.sh`.

### Dependencies

To use `Crossroads`, you must have the following dependencies
installed:

- [`Python`](https://www.python.org/)
- `Python` packages (`pip install -r requirements.txt`)
- [`Faust`](https://github.com/grame-cncm/faust)
- Mac/Linux only
  - Boost (`sudo apt-get install libboost-all-dev`)
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

### Running
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

# Run tests
./run_tests.sh
```

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

## TODO:

- Optimize parameters for a given structure
- Genetic algorithm to evolve structures
- Simple nonlinear elements
- Test cases:
  - LPF (other 2nd order filters...)
  - Simple reverb
  - Simple distortion with filtering

## License

GPL??
