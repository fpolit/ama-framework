#base plugin class
from .plugin import Plugin

# base cracked plugins
from .cracker import PasswordCracker

# base auxiliary plugins
from .auxiliary.auxiliary import Auxiliary


# password cracker plugins
from .cracker import (
    John,
    Hashcat,
    Hydra
)

# auxiliary plugins
from .auxiliary.wordlists import (
    Cupp
)

# from .auxiliary.hashes import (
#     Cupp
# )

# from .auxiliary.analysis import (
#     Cupp
# )
