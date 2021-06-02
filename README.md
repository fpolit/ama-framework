# ama - Attacks Manager

Ama is a specialized environment for the password cracking process. It contains several modules (attacks and auxiliaries), so you can find an appropiate module for each step of the password cracking process, also you can combine them to automatize the password cracking process (`auxiliaries` modules working as `preattack` or `postattack` of an `attack` module - we call them **fullattacks**: `preattack` + `attack` + `postattack`)

Also ama's attack modules can be submitted in a cluster of computers using `Slurm`, so you can perform **large** attacks, other important feature is that `ama` saves loots (cracked `hashes` and `services`) in a database and organize them (in *workspaces*) to enable efficient access to them. Finally, `ama` is easy extensible, so you can write custom modules to extend it.

## Dependencies
* [spack](https://spack.io/)
* [Hashcat](https://hashcat.net/hashcat/)
* [John](https://github.com/openwall/john) (with MPI support - Openmpi or MPICH (with slurm and pmix support))
* Postgresql
* [Hydra](https://github.com/vanhauser-thc/thc-hydra) (NO DEVELOPED ATTACKS MODULES YET)


Visit our [wiki](https://github.com/fpolit/ama-framework/wiki), there you can find guides to install them properly.
Also visit [depends](https://github.com/fpolit/ama-framework/tree/master/depends) directory, there you can find python scripts and spack packages to automatize ama's dependencies.


## Installation
* Users

```bash
    # Download some release (stable code)
    $ cd DOWNLOADED_AMA_RELEASE
    # I suggest you install ama in a python virtual enviroment (run: make virtualenv)
    $ make install
```

* Developers

If you want to contribute to `ama-framework` you are welcome.   
As developer you will first create a python virtual enviroment 
and then install `ama` and the developer packages.
```bash
    $ git clone https://github.com/fpolit/ama-framework.git ama
    $ cd ama
    $ make virtualenv_dev
    $ source env/bin/activate
    $ make pkgdev
```

**NOTE:**  
*Ama-framework* was tested in the following GNU/Linux distributions:
* Centos 8

## Usage
Visit our [wiki](https://github.com/fpolit/ama-framework/wiki), there you can find useful documentation about `ama`.  



     Please do not use ama in military or secret service organizations,
                      or for illegal purposes.



Good luck!  
            glozanoa
