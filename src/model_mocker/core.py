from typing import Any, Type, get_args, get_origin
from pydantic import BaseModel
import datetime

from .providers.string_provider import StringProvider
from .providers.number_provider import NumberProvider
from .providers.date_provider import DateProvider
from .providers.bool_provider import BoolProvider
from .providers.payment_provider import PaymentProvider


async def generate(model_class: Type[BaseModel]) -> BaseModel:
    """Generates a Pydantic model with dummy data."""
    fields: dict[str, Any] = await get_model_fields(model_class)
    values: dict[str, Any] = {}

    for name, field in fields.items():
        field_type: Any = await get_field_type(field)
        values[name] = await generate_field(field_type, name.lower())

    return model_class(**values)


async def generate_field(field_type: Any, field_name: str = "") -> Any:
    """Returns a dummy value based on the type and field name."""
    if field_type is str:
        fn = field_name.lower()
        if "credit" in fn or "card" in fn or fn.endswith("iban"):
            return PaymentProvider().credit_card_number()
        return StringProvider().handle(fn)

    if field_type is int:
        return NumberProvider().random_int()

    if field_type is float:
        return NumberProvider().random_float()

    if field_type is bool:
        return BoolProvider().random_bool()

    if field_type is datetime.date:
        return DateProvider().today()

    if get_origin(field_type) is list:
        inner = get_args(field_type)[0]
        return [await generate_field(inner, field_name) for _ in range(3)]

    if issubclass_safe(field_type, BaseModel):
        return await generate(field_type)

    # Fallback
    return None


async def get_model_fields(model_class: Type[BaseModel]) -> dict[str, Any]:
    """Abstraction layer for Pydantic v1 and v2 fields."""
    if hasattr(model_class, "model_fields"):
        return model_class.model_fields  # Pydantic v2
    elif hasattr(model_class, "__fields__"):
        return model_class.__fields__  # Pydantic v1
    else:
        raise ValueError("Unrecognized Pydantic version")


async def get_field_type(field: Any) -> Any:
    """Extracts the type of a Pydantic field."""
    if hasattr(field, "annotation"):  # Pydantic v2
        return field.annotation
    elif hasattr(field, "outer_type_"):  # Pydantic v1
        return field.outer_type_
    else:
        return field


async def issubclass_safe(cls: Any, base: type) -> bool:
    """Safe issubclass, without TypeError for non-types."""
    try:
        return issubclass(cls, base)
    except TypeError:
        return False
