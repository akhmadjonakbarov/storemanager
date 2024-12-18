from typing import Optional

from pydantic import BaseModel, Field


class DebtScheme(BaseModel):
    full_name: str = Field(max_length=100)
    phone_number: str = Field(max_length=9)
    phone_number2: Optional[str] = Field(None)
    amount: float = Field()
    address: str = Field()
