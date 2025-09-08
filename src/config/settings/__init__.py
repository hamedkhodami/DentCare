from os import getenv

from .base import *

PRODUCTION = int(getenv("PRODUCTION", 0))

if PRODUCTION:
    from .prod import *
else:
    from .dev import *
