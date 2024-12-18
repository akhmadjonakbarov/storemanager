from pydantic import BaseModel, Field


class CurrencyTypeScheme(BaseModel):
    name: str = Field(max_length=10)
