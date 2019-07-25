# solarpv-teamlabelling
A quick repo for collaboratively hand-labelling solar pv in remote sensing imagery

## Installation

### Download the repo

You can either [download](https://github.com/Lkruitwagen/solarpv-teamlabelling/archive/master.zip) and unzip it or clone it with git:

    git clone https://github.com/Lkruitwagen/solarpv-teamlabelling

then navigate to the repo:

    cd /your/path/to/solarpv-teamlabelling/

### Environment set up (recommended)

I use miniconda for environment setup. I've copied some venv instructions here as well.

#### - conda

For environment management with conda, create a conda environment:

    conda create --name labelpv python=3.6

Activate your conda environment:

    source activate labelpv

Install pip package manager to the environment:

    conda install pip

Install the project packages:

    pip install -r requirements.txt

#### - virtualenv (skip this if you are using conda)


Create the venv folder:

    python -m venv labelpv

Activate your virtual environment:

    source labelpv/bin/activate
    
Install the project packages:

    pip install -r requirements.txt
    
## Useage

Put your initials in the [google sheet](https://docs.google.com/spreadsheets/d/1u1OCc76FrySALuVD4UvJKnijdr2dJg23RNrP1eT0JIs/edit?usp=sharing) beside a container string. Copy the container string.

Contact me to get the .json file with the remote storage keys. Copy the .json file into the main directory.

Run the hand labelling client like so:

    python hand_label_client.py <REMOTE_STORAGE_CONTAINER>

This will:

1. create a new directory and download all the images for hand-labelling to that folder
2. then will display the images and request user input as to whether the image shows solar or not. See below.
3. user input will be logged in a `labels.json` file in the images directory.
4. `labels.json` will be periodically uploaded to remote storage.
5. once labelling is done, `labels.json` will be uploaded a final time and the 

### Labelling Solar PV

![typical sample](https://github.com/Lkruitwagen/solarpv-teamlabelling/blob/master/sample.png "Typical Sample")


You will be shown remote sensing imagery with the predicted solar PV outlined in cyan. The figure on the left is drawn from the Google basemap but may be outdated. The figure on the right is a recent image from Sentinel-2, a satellite constellation. You will be prompted to identify whether the image contains solar PV:

    CHOOSE {'a' -> solar; 's' -> not solar; '[' -> previous image; ']' -> next image; 'x' -> exit}; THEN [enter]

Enter 'a' for solar, 's' for not solar and then hit enter. '[' and ']' will cycle through the images. 'x' will exit. Your submissions will periodically be logged.

### Optional Arguments:

I haven't debugged all the option combinations, so just use one at a time (or help me out and write some debugging!)

* -d => Download only, useful for downloading several containers at once
* -nd => Skip the downloading, label images already downloaded
* -l => Run only the labelling locally, useful for downloading and labelling off-line
* -p => Immediately push local labels to remote storage
* -c => Clean up images at the end of the labelling
* -co => Immediately clean up image folder

Example syntax for using options:

    python hand_label_client.py <REMOTE_STORAGE_CONTAINER> -d=True