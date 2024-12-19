from typing import Optional

from pydantic import BaseModel, Field


class CustomerScheme(BaseModel):
    full_name: str = Field(
        default="John Smith",
        description="Customer's full name", min_length=8
    )
    phone_number: str = Field(
        default="901237459",
        description="Customer's phone number", min_length=9
    )
    phone_number2: Optional[str] = Field(

        "", description="Customer's secondary phone number",

    )
    address: str = Field(description="Customer's address")
