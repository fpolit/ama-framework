# ama - Attacks Manager

Ama is a specialized environment for the password cracking process. It contains several modules (attacks and auxiliaries), so you can find an appropiate module for each step of the password cracking process, also you can combine them to automatize the password cracking process (`auxiliaries` modules working as `preattack` or `postattack` of an `attack` module - we call them **fullattacks**: `preattack` + `attack` + `postattack`)

Also ama's attack modules can be submitted in a cluster of computers using `Slurm`, so you can perform **large** attacks, other important feature is that `ama` saves loots (cracked `hashes` and `services`) in a database and organize them (in *workspaces*) to enable efficient access to them. Finally, `ama` is easy extensible, so you can write custom modules to extend it.

## Dependencies
* [Hashcat](https://hashcat.net/hashcat/) (Only for hashcat attack modules)
* [John](https://github.com/openwall/john) (with MPI support - Openmpi or MPICH (with slurm and pmix support))(Only for john attack modules)
* [Hydra](https://github.com/vanhauser-thc/thc-hydra) (NO DEVELOPED ATTACKS MODULES YET)


Visit our [wiki](https://github.com/fpolit/ama-framework/wiki), there you can find guides to install them properly.
Also visit [depends](https://github.com/fpolit/ama-framework/tree/master/depends) directory, there you can find python scripts and spack packages to automatize ama's dependencies.

**NOTE:**  
*Ama-framework* was tested in the following GNU/Linux distributions:
* Centos 8

## Usage
Visit our [wiki](https://github.com/fpolit/ama-framework/wiki), there you can find useful documentation about `ama`.  



     Please do not use ama in military or secret service organizations,
                      or for illegal purposes.



Good luck!  
            glozanoa
