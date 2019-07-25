# solarpv-teamlabelling
A quick repo for collaboratively hand-labelling solar pv in remote sensing imagery

## Installation

There are two ways to set up your development environment. The preferred being [conda](https://docs.conda.io/en/latest/miniconda.html), but if you have problems with that set up then you can use virtualenv instead.

### For conda

For environment management with conda, first check the version of python at [runtime.txt](/runtime.txt). Then create a conda environment:

    conda create --name oxeo-app python=X.X.X

Activate your conda environment:

    source activate oxeo-app

Install pip package manager to the environment:

    conda install pip

Install the project packages:

    pip install -r requirements.txt

### For virtualenv (skip this if you are using conda)

Ensure that you're running the correct version of Python. See [runtime.txt](/runtime.txt) to see what is running in production. If you need to run multiple versions of python consider using [pyenv](https://github.com/pyenv/pyenv).

Create the venv folder:

    python -m venv oxeo-app

Activate your virtual environment:

    source oxeo-app/bin/activate
    
Install the project packages:

    pip install -r requirements.txt
    
## Useage
