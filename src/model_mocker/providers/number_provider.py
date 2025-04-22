from faker import Faker

class NumberProvider:
    """Creates dummy numbers (int & float)."""
    faker = Faker()

    def random_int(self, min: int = 0, max: int = 100) -> int:
        return self.faker.random_int(min=min, max=max)

    def random_float(self, min: float = 1.0, max: float = 100.0, precision: int = 2) -> float:
        val = self.faker.pyfloat(min_value=min, max_value=max, right_digits=precision)
        return float(f"{val:.{precision}f}")
