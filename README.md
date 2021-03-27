# ama - Attack Manager

Ama is a specialized environment for the password cracking process. It contains several modules (attacks and auxiliaries) that make the password cracking process efficient (using auxiliary modules as helper modules of attacks).
Also ama's attack modules can be submitted in a cluster using `Slurm`, other important feature is that ama is easy extensible so you can write your own modules.

## Dependences
* Hashcat
* Hydra
* pmix
* Openmpi (with slurm and pmix support)
* John The Ripper (with MPI support)
* HPC Cluster (needed to submit parallel tasks with slurm)

Visit our [wiki](https://github.com/fpolit/ama-framework/wiki), there you can find guides to install them properly.


## Installation
* Users

```bash
    # Download some release (stable code)
    $ cd DOWNLOADED_AMA_RELEASE
    # I suggest you install ama in a python virtual enviroment
    $ make install
```

* Developers

If you want to contribute to `ama-framework` you are welcome.   
As developer you will first create a python virtual enviroment 
and then install `ama` and the developer packages.
```bash
    $ git clone https://github.com/fpolit/ama-framework.git ama
    $ cd ama
    $ make virtualenv
    $ source env/bin/activate
    $ make installdev
```

## Usage
Visit our [wiki](https://github.com/fpolit/ama-framework/wiki), there you can find useful documentation about `ama`.  



     Please do not use ama in military or secret service organizations,
                      or for illegal purposes.



Good luck!  
            glozanoa
