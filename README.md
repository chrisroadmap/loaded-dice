# loaded-dice
Investigating the impact of climate uncertainty on climate economics using a simple cost-benefit IAM. Note this is still a work in progress and many things need to be improved.

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
