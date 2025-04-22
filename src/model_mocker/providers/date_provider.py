import datetime
from faker import Faker

class DateProvider:
    """Creates date objects or date strings."""
    faker = Faker()

    def today(self) -> datetime.date:
        return datetime.date.today()

    def past_date(self) -> datetime.date:
        return self.faker.date_object()

    def date_string(self, fmt: str = "%Y-%m-%d") -> str:
        return self.faker.date(pattern=fmt)
