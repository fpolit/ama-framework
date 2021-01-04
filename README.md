# mattack
`mattack` is an integrator of [PPACK](https://gitlab.com/spolit/ppack) and a `pasword cracker`(hashcat or john the ripper) to perform `mask attacks` against an hash.

### Dependences
Visit our [wiki](https://gitlab.com/spolit/mattack/-/wikis/home), there you can find guides to install properly `Openmpi` and `Jhon The Ripper`

* Openmpi (with slurm support)
* John The Ripper (with MPI support)
* Hashcat (needed only for massively parallel mask attacks)


### Installation
* From `Pypi`
```bash
    python3 -m pip install mattack
```

* From `gitlab` source code
```bash
    git clone https://gitlab.com/spolit/mattack.git
    cd mattack
    make install
```

### Usage
Visit our [wiki](https://gitlab.com/spolit/mattack/-/wikis/home), there you can find a full documentation of `mattack`.  
