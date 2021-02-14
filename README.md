# aman - Attack Manager
Initially `aman` was a simple integrator of [PPACK](https://gitlab.com/spolit/ppack) (mask generator) and a `password cracker`(`hashcat` or `john the ripper`) to perform `mask attacks` against hashes submiting parallel tasks in a cluster using `Slurm`. Then we extend it to perform diverse attacks (wordlist attacks, combination attacks, hybrid attacks [wordlist + masks or masks + wordlist] and of course mask attacks). But now it also support `hydra` cracker, so you can perform attacks again services (supported by `hydra`) submiting parallel task in a cluster.

### Dependences
* Openmpi (with slurm and pmix support)
* John The Ripper (with MPI support)
* Hashcat (to perform attacks using the GPU power)
* Hydra (to perform attacks again services)
* HPC Cluster (needed to submit parallel tasks in a cluster with slurm)

Visit our [wiki](https://gitlab.com/spolit/aman/-/wikis/home), there you can find guides to install properly `Openmpi`, `Jhon The Ripper` and configure an `HPC cluster`


### Installation

```bash
    git clone https://gitlab.com/spolit/aman.git
    cd aman
    make install
```

### Usage
Visit our [wiki](https://gitlab.com/spolit/aman/-/wikis/home), there you can find useful documentation about `aman`.  


**NOTE: DO NOT USE `aman` IN ILLEGAL ACTIVITIES**

Happy Hacking!  
~ glozanoa
