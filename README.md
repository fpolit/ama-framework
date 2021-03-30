# ama - Attack Manager

Ama is a specialized environment for the password cracking process. It contains several modules (attacks and auxiliaries), so we can combine them (`auxiliaries` modules as `preattack` or `postattack` of an `attack` module - we call them `fullattacks`: `preattack` + `attack` + `postattack`) to make the password cracking process efficient.
Also ama's attack modules can be submitted in a cluster of computers using `Slurm`, so you can perform **large** attacks, other important feature is that ama is easy extensible, so you can write your own modules.

## Dependences
* Hashcat (only if you are going to perform attacks against hashes using GPU power)
* Hydra (only if you are going to perform attacks against services)
* pmix
* Openmpi (with slurm and pmix support)
* John The Ripper (with MPI support) (only if you are going to perform attacks against hashes using CPU power)
* HPC Cluster (only if you are going to submit attacks in a cluster of computers with ```Slurm`)

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
