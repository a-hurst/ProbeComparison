# ProbeComparison

ProbeComparison is the experiment program for a study exploring how the phrasing and format of different mind-wandering probes affect the measurement of mind-wandering rates and effects. This study compares overall rates of mind-wandering and magnitudes of time-on-task effects in a SART task across different different types of probes (between subjects, see table below).

![SART with Mason et al. (2007) probe](probecompare.gif)

The probe formats and phrasings are taken from the top-5 cited papers studying mind-wandering with probes from 2003 to 2018. The ultimate aim of this study is to investigate the differences in how mind-wandering is measured between common probe types, and assess whether any of these differences are large enough for methodological concern.


## Requirements

ProbeComparison is programmed in Python 2.7 (3.3+ compatible) using the [KLibs framework](https://github.com/a-hurst/klibs). It has been developed and tested on macOS (10.9 through 10.14), but should also work with minimal hassle on computers running [Ubuntu](https://www.ubuntu.com/download/desktop) or [Debian](https://www.debian.org/distrib/) Linux, as well as on computers running Windows 7 or newer with [a bit more effort](https://github.com/a-hurst/klibs/wiki/Installation-on-Windows).

## Getting Started

### Installation

First, you will need to install the KLibs framework by following the instructions [here](https://github.com/a-hurst/klibs).

Then, you can then download and install the experiment program with the following commands (replacing `~/Downloads` with the path to the folder where you would like to put the program folder):

```bash
cd ~/Downloads
git clone https://github.com/a-hurst/ProbeComparison.git
```


### Running the Experiment

ProbeComparison is a KLibs experiment, meaning that it is run using the `klibs` command at the terminal (running the 'experiment.py' file using Python directly will not work).

To run the experiment, navigate to the ProbeComparison folder in Terminal and run `klibs run [screensize]`,
replacing `[screensize]` with the diagonal size of your display in inches (e.g. `klibs run 24` for a 24-inch monitor). If you just want to test the program out for yourself and skip demographics collection, you can add the `-d` flag to the end of the command to launch the experiment in development mode.

#### Choosing the Probe Type

This experiment program allows you to specify which of the five probe types to use on launch. To do so, simply launch the experiment with the condition flag set to one of the following values:

Condition Flag | Data Label | Probe Format
--- | --- | ---
`a` | `christoff2009` | [Christoff, Gordon, Smallwood, Smith, & Schooler (2009)](https://doi.org/10.1073/pnas.0900234106)
`b` | `mcvay2009` | [McVay & Kane (2009)](https://doi.org/10.1037/a0014104)
`c` | `mason2007` | [Mason et al. (2007)](https://doi.org/10.1126/science.1131295)
`d` | `killingsworth2010` | [Killingsworth & Gilbert (2010)](https://doi.org/10.1126/science.1192439)
`e` | `mrazek2013` | [Mrazek, Franklin, Phillips, Baird, & Schooler (2013)](https://doi.org/10.1177/0956797612459659)

For example, to run the experiment using the probe format from McVay & Kane (2009), you would launch the experiment using `klibs run 24 --condition b`.


### Exporting Data

To export data from ProbeComparison, simply run 

```
klibs export
```

while in the ProbeComparison directory. This will export the trial data for each participant into individual tab-separated text files in the project's `ExpAssets/Data` subfolder.
