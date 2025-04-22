from faker import Faker

class StringProvider:
    """Creates dummy strings for typical text fields."""
    faker = Faker()

    def name(self) -> str:
        return self.faker.name()

    def email(self) -> str:
        return self.faker.email()

    def username(self) -> str:
        return self.faker.user_name()

    def password(self) -> str:
        return self.faker.password()

    def address(self) -> str:
        return self.faker.address()

    def company(self) -> str:
        return self.faker.company()

    def city(self) -> str:
        return self.faker.city()

    def country(self) -> str:
        return self.faker.country()

    def url(self) -> str:
        return self.faker.url()

    def uuid(self) -> str:
        return str(self.faker.uuid4())

    def word(self) -> str:
        return self.faker.word()

    def slug(self) -> str:
        return self.faker.slug()
    
    def phone(self) -> str:
        return self.faker.basic_phone_number()


    def handle(self, field_name: str) -> str:
        """Dispatch based on the field name."""
        fn = field_name.lower()
        if "email" in fn:
            return self.email()
        if "name" in fn:
            return self.name()
        if "username" in fn or fn == "user":
            return self.username()
        if "password" in fn or "pass" in fn:
            return self.password()
        if "address" in fn:
            return self.address()
        if "company" in fn:
            return self.company()
        if "city" in fn:
            return self.city()
        if "country" in fn:
            return self.country()
        if "url" in fn or "link" in fn:
            return self.url()
        if "uuid" in fn or fn.endswith("_id"):
            return self.uuid()
        if "slug" in fn:
            return self.slug()
        if "phone" in fn:
            return self.phone()
        # Fallback
        return self.word()
