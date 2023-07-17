# loaded-dice

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.7682442.svg)](https://doi.org/10.5281/zenodo.7682442)

Investigating the impact of climate uncertainty on climate economics using a simple cost-benefit IAM (DICE) with the climate component updated with a calibrated, constrained Monte Carlo ensemble of the FaIR model (v2.1). Paper in review.

A pre-print is available at https://arxiv.org/abs/2304.08957.

![Effect of varying climate uncertainty on projections](figures/projections_scc_ecs.png?raw=true)

## Requirements
- A licensed version of GAMS. Maybe I'll make a python version in the future.
- Python 3.7+ and Anaconda

## Reproduction
1. Clone the repository. If you think you will want to make changes, it's best to fork it first, then clone your fork.
2. Navigate to your local working copy, create an environment and install dependencies:

`conda env create -f environment.yml`

3. Activate environment

`conda activate loaded-dice`

4. Run the scripts in numerical order from the `scripts` directory

`python scripts/<script_name.py>`

## Notes and acknowledgements
The `dice2016` and `dice2023` folders contain supplementary GAMS code from the online appendix of [Barrage & Nordhaus (2023)](https://www.nber.org/papers/w31112). The original source of this material is [here](https://bit.ly/3TwJ5nO). In order to present results from these simulations with DICE2016 and DICE2023 for full reproducibility, the GAMS code and the output CSV results have been included in this repository. No clear licence was provided for these files. The attribution for this source code should go to Barrage & Nordhaus.
