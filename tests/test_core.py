import pytest
import re
from pydantic import BaseModel
from src.model_mocker.core import generate


class TestModel(BaseModel):
    name: str
    email: str
    phone: str
    age: int
    height: float
    active: bool


@pytest.mark.asyncio
async def test_generate_string_fields():
    instance = await generate(TestModel)

    assert isinstance(instance.name, str)
    assert " " in instance.name

    assert isinstance(instance.email, str)
    assert re.match(r"[^@]+@[^@]+\.[^@]+", instance.email)

    assert isinstance(instance.phone, str)
    assert any(char.isdigit() for char in instance.phone)


@pytest.mark.asyncio
async def test_generate_other_fields():
    instance = await generate(TestModel)

    assert isinstance(instance.age, int)
    assert 0 <= instance.age <= 100

    assert isinstance(instance.height, float)
    assert 1.0 <= instance.height <= 100.0

    assert isinstance(instance.active, bool)
