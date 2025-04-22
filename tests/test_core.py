import pytest
import re
import datetime
from pydantic import BaseModel

from src.model_mocker.providers.string_provider import StringProvider
from src.model_mocker.providers.number_provider import NumberProvider
from src.model_mocker.providers.date_provider import DateProvider
from src.model_mocker.providers.bool_provider import BoolProvider
from src.model_mocker.providers.payment_provider import PaymentProvider
from src.model_mocker.core import generate_field


# ---------------------------
# Tests for Provider Classes
# ---------------------------

def test_string_provider_basic_methods():
    sp = StringProvider()
    # deterministic outputs for tests
    sp.faker.seed_instance(0)

    name = sp.name()
    assert isinstance(name, str) and len(name) > 0

    email = sp.email()
    assert isinstance(email, str)
    assert re.match(r"[^@]+@[^@]+\.[^@]+", email)

    username = sp.username()
    assert isinstance(username, str) and len(username) > 0

    password = sp.password()
    assert isinstance(password, str) and len(password) >= 6

    address = sp.address()
    assert isinstance(address, str) and any(char.isdigit() for char in address)

    company = sp.company()
    assert isinstance(company, str) and len(company) > 0

    city = sp.city()
    assert isinstance(city, str) and len(city) > 0

    country = sp.country()
    assert isinstance(country, str) and len(country) > 0

    url = sp.url()
    assert isinstance(url, str) and url.startswith(('http://', 'https://'))

    uuid = sp.uuid()
    assert isinstance(uuid, str)
    assert re.match(r"[0-9a-f-]{36}", uuid)

    word = sp.word()
    assert isinstance(word, str)
    assert re.match(r"\w+", word)

    slug = sp.slug()
    assert isinstance(slug, str)
    assert len(slug) > 0


def test_string_provider_handle_dispatch():
    sp = StringProvider()
    sp.faker.seed_instance(1)

    assert re.match(r"[^@]+@[^@]+\.[^@]+", sp.handle('email'))
    assert ' ' in sp.handle('name')
    assert isinstance(sp.handle('username'), str)
    assert isinstance(sp.handle('password'), str)
    assert any(char.isdigit() for char in sp.handle('address'))
    assert isinstance(sp.handle('company'), str)
    assert isinstance(sp.handle('city'), str)
    assert isinstance(sp.handle('country'), str)
    assert sp.handle('url').startswith(('http://', 'https://'))
    assert re.match(r"[0-9a-f-]{36}", sp.handle('order_id'))
    assert isinstance(sp.handle('slug'), str)
    # fallback
    assert isinstance(sp.handle('unknown_field'), str)


def test_number_provider_methods():
    np = NumberProvider()
    np.faker.seed_instance(2)

    i = np.random_int(min=5, max=10)
    assert isinstance(i, int)
    assert 5 <= i <= 10

    f = np.random_float(min=0.5, max=1.5, precision=3)
    assert isinstance(f, float)
    # check precision
    assert len(str(f).split('.')[-1]) <= 3


def test_date_provider_methods():
    dp = DateProvider()

    today = dp.today()
    assert isinstance(today, datetime.date)
    assert today == datetime.date.today()

    past = dp.past_date()
    assert isinstance(past, datetime.date)

    ds = dp.date_string(fmt="%Y/%m/%d")
    assert isinstance(ds, str)
    assert re.match(r"\d{4}/\d{2}/\d{2}", ds)


def test_bool_provider_method():
    bp = BoolProvider()
    vals = {bp.random_bool() for _ in range(20)}
    assert vals.issubset({True, False})
    # expect both True and False over multiple draws
    assert True in vals and False in vals


def test_payment_provider_methods():
    pp = PaymentProvider()
    pp.faker.seed_instance(3)

    cc = pp.credit_card_number()
    assert isinstance(cc, str)
    assert any(char.isdigit() for char in cc)

    cvv = pp.credit_card_cvv()
    assert isinstance(cvv, str)
    assert cvv.isdigit() and 3 <= len(cvv) <= 4

    iban = pp.iban()
    assert isinstance(iban, str)
    assert re.match(r"[A-Z]{2}\d+", iban)

    bban = pp.bank_account()
    assert isinstance(bban, str)
    # BBAN can be alphanumeric
    assert bban.isalnum()


# ---------------------------------
# Tests for core.generate_field
# ---------------------------------

class Dummy(BaseModel):
    x: int

class Container(BaseModel):
    values: list[int]
    dummy: Dummy

@pytest.mark.asyncio
async def test_generate_field_primitives():
    # string fallback
    s = await generate_field(str, 'unknown')
    assert isinstance(s, str)

    e = await generate_field(str, 'email')
    assert '@' in e

    i = await generate_field(int, 'count')
    assert isinstance(i, int)

    f = await generate_field(float, 'ratio')
    assert isinstance(f, float)

    b = await generate_field(bool, 'flag')
    assert isinstance(b, bool)

    d = await generate_field(datetime.date, 'date')
    assert isinstance(d, datetime.date)


@pytest.mark.asyncio
async def test_generate_field_list_and_nested():
    # list of ints
    lst = await generate_field(list[int], 'items')
    assert isinstance(lst, list)
    assert all(isinstance(v, int) for v in lst)

    # nested pydantic model
    dummy = await generate_field(Dummy, 'dummy')
    assert isinstance(dummy, Dummy)
    assert isinstance(dummy.x, int)

    # container with list and nested
    cont = await generate_field(Container, 'container')
    assert isinstance(cont, Container)
    assert isinstance(cont.values, list) and all(isinstance(v, int) for v in cont.values)
    assert isinstance(cont.dummy, Dummy)
