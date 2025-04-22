import random

class BoolProvider:
    """Creates random booleans."""
    def random_bool(self) -> bool:
        return random.choice([True, False])
