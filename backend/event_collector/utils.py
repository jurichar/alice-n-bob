"""
utils.py is the file that contains VERY useful functions.
"""

import random
import uuid

CONSONANTS = "bcdfghjklmnprstvwz"
VOWELS = "aeuio"


def generate_name() -> str:
    """Generate a semi-readable ID. Can be considered globally unique."""
    cs = random.choices(CONSONANTS, k=3)
    vs = random.choices(VOWELS, k=3)
    name = "".join(cs[i] + vs[i] for i in range(3))
    return name + "-" + str(uuid.uuid4())[:8]
