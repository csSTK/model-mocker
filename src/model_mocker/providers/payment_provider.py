from faker import Faker

class PaymentProvider:
    """Generates payment data consisting only of numbers."""
    faker = Faker()

    def credit_card_number(self) -> str:
        return self.faker.credit_card_number(card_type=None)

    def credit_card_cvv(self) -> str:
        return self.faker.credit_card_security_code()

    def iban(self) -> str:
        return self.faker.iban()

    def bank_account(self) -> str:
        return self.faker.bban()
