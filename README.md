# hattack - hash attack
Initially `hattack` was simply an integrator of [PPACK](https://gitlab.com/spolit/ppack) (mask generator) and a `pasword cracker`(hashcat or john the ripper) to perform `mask attacks` against an hash submiting parallel tasks in a cluster using `Slurm`. But we extend it to perform diverse attacks (wordlist attacks, combination attacks, hybrid attacks [wordlist + masks or masks + wordlist] and of course mask attacks)

### Dependences
* Openmpi (with slurm support)
* John The Ripper (with MPI support)
* Hashcat (needed for massively parallel mask attacks)
* HPC Cluster (needed to submit parallel tasks in a cluster with slurm)

Visit our [wiki](https://gitlab.com/spolit/hattack/-/wikis/home), there you can find guides to install properly `Openmpi`, `Jhon The Ripper` and configure an `HPC cluster`


### Installation

```bash
    git clone https://gitlab.com/spolit/hattack.git
    cd hattack
    make install
```

### Usage
Visit our [wiki](https://gitlab.com/spolit/hattack/-/wikis/home), there you can find useful documentation of `hattack`.  


Happy Hacking!
