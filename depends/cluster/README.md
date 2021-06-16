# Usage
In this guide I show you how you will use *python* scripts to install a package.
* Installing script dependencies

  Before we install any package we need create a virtual enviroment, to do that I going to use `virtualenv` rule of [Makefile](https://github.com/fpolit/ama-framework/blob/master/Makefile)
  ```bash
   # I am in AMA_REPO
   $ make virtualenv
   $ source env/bin/activate
  ```
  * Installing packages in [requirements.txt](https://github.com/fpolit/ama-framework/blob/master/depends/cluster/requirements.txt)
  
  To run *python scripts* we need install some python packages in ouw created virtual enviroment.
  ```bash
  # I am in AMA_REPO/depends/cluster
  $ python3 -m pip install -r requirements.txt
  ```
  
  * Installing *CentOS* dependencies  
  
  Each script need some *CentOS* packages, so you can install them using [centos requirements](https://github.com/fpolit/ama-framework/blob/master/depends/cluster/centos_requirements.py) script as follow:
  ```bash
    $ python3 centos_requirements.py
  ```
  
  Now we are ready to run scripts to install som packages. If you want to perform attacks in a cluster of computers then install **Slurm** packages 
  otherwise (you only want to run attack localy) install only **John**.

* Installing *Slurm*

To install *Slurm* you need to install *munge*, and *pmix* (which needs of *munge* package). So first we are going to install *munge*
  * Munge installation
  
    ```bash
    # Im am in AMA_REPO/depends/cluster
    $ python3 munge.py -c build
    ```
    The above command will create a directory called **build** (if it doesn't exist) where **munge-0.5.14.tar.gz** will be downloaded, uncompressed , 
    compiled and intalled in appropriate places (check the script for more detail).
    
  * Pmix Installation
  
    ```bash
    # Im am in AMA_REPO/depends/cluster
    $ python3 pmix.py -c build
    ```
    The above command will create a directory called **build** (if it doesn't exist) where **pmix-3.2.3.tar.gz** will be downloaded, uncompressed , 
    compiled and intalled in *appropriate places* (check the script for more detail).

**NOTE**:
No one (munge and pmix) need be added to the **PATH**, because they were installed in *appropriate places* (perhaps the only thing that you need is update your terminal) 

Now at this point we have installed *Pmix* and *Munge* (Slurm's dependencies), so to install *Slurm*, simply run:
```bash
# I am in AMA_REPO/depends/cluster
$ python3 slurm.py -c build
```
The above command will create a directory called **build** (if it doesn't exist) where **pmix-3.2.3.tar.gz** will be downloaded, uncompressed , 
compiled and intalled in *appropriate places* (check the script for more detail).

Finally, the Slurm's configuration files are in `/etc/slurm-llnl` directory.

* Installing *John*

To install *john* you need to install *OpenMPI*, and to install *OpenMPI* you need *pmix* which needs of *munge* package. 

  * Installing Munge and Pmix
 
    If you have installed **Slurm**, then you have installed both packages, otherwise check *Slurm* installation.
    
  * Installing OpenMPI
  
  ```bash
    # I am in AMA_REPO/depends/cluster
    $ python3 openmpi.py -c build --prefix=/usr/local/openmpi
  ```
  The above command will create a directory called **build** (if it doesn't exist) where **openmpi-4.1.1.tar.gz** will be downloaded, uncompressed, 
  compiled and installed in `/usr/local/openmpi` directory.
  
Now at this point you have installed all John's dependencies, so to install it simply run:
```bash
  # I am in AMA_REPO/depends/cluster directory 
  $ python3 john.py -c JOHN_HOME
  # JOHN_HOME: is a directory where do you want to install john
```

**NOTE**:
`JOHN_HOME` directory will be a directory with write permission.
