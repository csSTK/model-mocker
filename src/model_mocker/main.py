from typing import Optional
from pydantic import BaseModel
from model_mocker.core import generate
import asyncio


class User(BaseModel):
    name: str
    email: str
    phone: str
    address: str
    age: int
    is_active: Optional[bool] | None


async def main():
    user = await generate(User)
    print(user)


if __name__ == "__main__":
    asyncio.run(main())
