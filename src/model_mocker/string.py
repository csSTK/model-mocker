from faker import Faker

faker = Faker()


async def check_string(value: str) -> str:
    value = value.lower()

    if "email" in value or "mail" in value:
        return faker.email()
    elif "name" in value:
        return faker.name()
    elif "phone" in value or "tel" in value:
        return faker.phone_number()
    return faker.word()
