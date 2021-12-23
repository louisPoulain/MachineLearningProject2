# Python code for ModalPINN

## Context

Python code to define, train and output ModalPINNs as defined in the paper

> _ModalPINN : an extension of Physics-Informed Neural Networks with enforced truncated Fourier decomposition for periodic flow reconstruction using a limited number of imperfect sensors._ Gaétan Raynaud, Sébastien Houde, Frédérick P. Gosselin (2021) 

Contact email : gaetan.raynaud (at) polymtl.ca 

EDIT:
The code has been updated to work on EPFL clusters and has been modified in order to test new data sets and create new comparisons
Contact email : louis.poulain-auzeau@epfl.ch _or_ kevin.rizk@epfl.ch


**The code has been re-designed to work on EPFL cluster izar with very specific conditions. Please follow precisely this readME**
Note that there are functions to restore the neural network with weights and biases that we have found. This way, if you don't have access to the cluster, you may still be able to see the results.


## How to prepare the cluster and how to download data

1. connect to Izar cluster (ssh -X username@izar.epfl.ch)

2. download everything from this directory into you working directory : git clone thisFolderWebAdress :
    - *create a new folder* named data : mkdir data 
    - *check* that this folder is in the parent directory of the folder containing the git
    - *download* the first data set (low Reynolds number) from the website : 
        - *wget* https://zenodo.org/record/5039610/files/fixed_cylinder_atRe100?download=1
    - *rename* the file "fixed_cylinder_atRe100" : mv fixed_cylinder_atRe100?download=1 fixed_cylinder_atRe100
3. *load* required modules : module load gcc cuda/10.0.130 cudnn/7.4.2.24-10.0-linux-x64 python mvapich2)
4. *create* virtual python environment : virtualenv --system-site-packages venv)
5. *activate* virtual env : source ../venv/bin/activate
6. *install* requirements : pip install -r requirements.txt
7. *deactivate* virtual env : deactivate
8. *launch* the .run file : sbatch MPinn.run

In the end you should have folders organised the following way:
- *home*
    - *Data*, *git_repo*
        - *Data* : fixed_cylinder_atRe100 
        
If you don't you can use the command "mv" to move the files as you wish : mv name_file  destination


## How to upload the other data sets:
The other data sets have been uploaded on a drive google. You can find the first folder here: https://drive.google.com/drive/folders/1iOyjurASeyk64mdoAqfKv7jQWvssLNsO?usp=sharing and the second one here: https://drive.google.com/drive/folders/1bok-LbcQJ-XJ1tQISQE3-6v4hBUYPVYA?usp=sharing
The first folder contains the laminar data sets (low Re) and the other the turbulent data sets (high Re).

If you have access, you can manually download them on your local machine.
Then : 
1. open a terminal.
2. enter : sftp username@izar.epfl.ch
3. go to the folder Data : cd Data/
4. upload the new data sets : put path_of_data_sets _or_ put -r path_to_folder_containing_data_sets
5. you may have to rename the files in the folder Steady_sampling by removing the extension ".dat" (or be careful when running the python script)


## How to download files from the clusters ?
You can use the scp command to dowload files from the cluster. Alternatively you can also clone the git repository onto your local machine

- *with scp* : scp username@izar.epfl.ch:path_to_the_file_in_the_cluster/file.extension /path_to_where_you_want_to_put_it/
- *with git* : - *git add* name_file_to_add _or_ git add -A (to add everything)
               - *git commit* -m 'commit_message'
               - *git push*

To find the paths can use the command "pwd"


## Files

The main files are :
- *ModalPINN_VortexShedding.py* : performs flow reconstruction using ModalPINN with dense or sparse data, possibly with out of synchronisation or gaussian noise (see the argument to the parser). It requires:
    - *Load_train_data_desync.py*:
        Python file containing functions that extract and prepare data for training and validation.
    - *NN_functions.py*:
        Python file containing functions specific to neural networks, optimisers and plots.
- *ClassicPINN_VortexShedding.py* : define a PINN for performance comparison with ModalPINN on dense data. It requires:
    - *NN_functions_classicPINN.py* which translates the same functions than in NN_functions.py but without the modal approach
- *reactions_process.py* and *text_flow.py* provided by M. Boudina to read data sets (see the training data section below)
WARNING : text_flow.py has been modified a bit from the version of M. Boudina to accept new data sets and perform automatic normalisation of the data. Since the data provided by M. Boudina is already normalised, you might have to change the end of the code to suppress the automatic normalisation when using the data "fixed_cylinder_atRe100".
- *visualisation_ground_truth.py* : contains script to create plots in order to compare with the model approximation and the ground truth
- *visualisation_mode_shape.py* : contains script to visualise the mode shapes
- *forces* : contains a script that plot the approximated forces for one specific job. This could modify to accept any of our files now (we export now also the forces).

## How to run basic jobs

This code is designed to be launched on a computationel cluster (initially for Graham server on Compute Canada) using the following batch commands:

    #!/bin/bash
    #SBATCH --gres=gpu:1
    #SBATCH --cpus-per-task=2
    #SBATCH --mem=50G
    #SBATCH --job-name=ModalPINN_modalEQ
    #SBATCH --time=0-10:00

    module purge
    module load gcc
    module load cuda/10.0.130
    module load cudnn/7.4.2.24-10.0-linux-x64
    source ../venv/bin/activate
    python ./ModalPINN_VortexShedding.py --Tmax 8 --Nmes 5000 --Nint 8000 --multigrid --Ngrid 5 --NgridTurn 200 --WidthLayer 25 --Nmodes 2 --BothEquations --SparseData --DataLocation cylinder_pitot --TwoZonesSampling
deactivate

There are multiple arguments that you can pass to the script, please check the ModalPINN_VortexShedding.py file for more information.


For each job launched, a folder is created in ./OutputPythonScript_Surrogates and is identified by several informations on the arguments used. In this folder, the content of console prints is saved in *out.txt* including the model itself in a pickle archive. Also lots of data are saved into pickle archives in order to produce plots afterwards.
There are already lots of jobs that we launch. You can restore the neural network we had using the file DNN2_80_80_4.pickle and the functions in NN_functions.py.

## Requirements

This code has been tested and used with the following versions of environments and libraires and may not be directly compatible with other versions (especially with tensorflow>=2.0)

Environments in Compute Canada

    StdEnv/2020
    nixpkgs/16.09
    python/3.7.4
     
Python libraries

    numpy==1.17.4
    scipy==1.3.2
    tensorflow_gpu==1.14.1
    matplotlib==3.1.1
     
For a more detailed list of python libraries, see *requirements.txt*. You can also set up an environment with

    virtualenv --no-download ~/ENV
    source ~/ENV/bin/activate
    pip install --upgrade pip
    python pip install -r requirements.txt

## Training data

Training data presented in the paper was provided by Boudina et al. 
> Boudina, M., Gosselin, F., & Étienne, S. (2021). Vortex-induced vibrations: A soft coral feeding strategy? Journal of Fluid Mechanics, 916, A50. doi:10.1017/jfm.2021.252 

and is available for download on Zenodo
> Boudina, Mouad. (2021). Numerical simulation data of a two-dimensional flow around a fixed circular cylinder [Data set]. Zenodo. http://doi.org/10.5281/zenodo.5039610  [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5039610.svg)](https://doi.org/10.5281/zenodo.5039610)

along with two python scripts (*reactions_process.py* and *text_flow.py*) that perform the reading of these data files.

Nonetheless other data can be used. Provided functions in *Load_train_data_desync.py* might be reused if the structure of data suits [time step,element id] for u,v,p and a list of x,y [element id]. Otherwise, it might be necessary to adapt these functions to your data structure.

## Provided results and import of previously trained ModalPINN

Some of the trained ModalPINN which results are plotted in the main paper are saved in the folders OutputPythonScript. Weights and biases values of the model are stored in a pickle archive and can be imported by using these lines  

    repertoire= 'OutputPythonScript/Name_of_the_folder'
    filename_restore = repertoire + '/DNN2_40_40_2_tanh.pickle' # Attention to change the name of .pickle depending of the NN layers
    w_u,b_u,w_v,b_v,w_p,b_p = nnf.restore_NN(layers,filename_restore)

instead of these:

    w_u,b_u = nnf.initialize_NN(layers)
    w_v,b_v = nnf.initialize_NN(layers)
    w_p,b_p = nnf.initialize_NN(layers)

## License

Codes are provided under license MIT
