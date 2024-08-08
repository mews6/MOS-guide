# MOS Guide
Modeling, Simulation and Optimization for the common man!



## Running the labs

For the examples provided of different use cases of optimization (called internally as 'Labs') i recommend using an Anaconda environment, mostly because solvers are more readily available and can be . you can get a copy of Miniconda, a minimal conda installer in [here](https://docs.anaconda.com/miniconda/), generally, everything you need for running the examples provided can be found on `requirements.txt`. They are, once again, mostly thought as meant to run under an anaconda environment.

### Configuring Anaconda.

For the purposes of this repository, you can get by with the installation guide provided for either [Anaconda](https://docs.anaconda.com/anaconda/install/) or [Miniconda](https://docs.anaconda.com/miniconda/miniconda-install/), these installation instructions will depend on your operating system and as such, you will have to follow the corresponding guide. However, once you have set up anaconda in your system, you can make a virtual environment for you to work on by inputting the following commands while having your terminal in the repository:

```
conda init 
conda create --name myenv
```

'myenv' can be changed to whatever name you want your environment to have, and shouldn't have any bearing on the execution of such profiles. Once you have that sorted out, it can be then initialized with the following command:

```
conda activate myenv
```

to install all relevant dependencies, go to the root of your project and run:

```
conda install --file requirements.txt
```

Once all this is said and done, you should be able to run any Python script found in this repository. You can test all dependencies were dealt with correctly by running the script `./labs/lab0/src/scripts/testBasics.py`