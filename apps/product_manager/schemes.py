from typing import List
from typing import Optional
from pydantic import BaseModel, Field


class ItemScheme(BaseModel):
    name: str = Field(min_length=4)
    barcode: str = Field(min_length=4)
    category_id: Optional[int] = Field(default=None, gt=0)
    unit_id: int = Field(gt=0)


class UnitScheme(BaseModel):
    value: str


class CategoryScheme(BaseModel):
    name: str = Field(min_length=4)


# Schema for the Currency object
class CurrencyScheme(BaseModel):
    id: Optional[int] = Field(None, description="Currency ID")


# Main schema for Document Item
class DocumentItemModelScheme(BaseModel):
    qty: float = Field(..., description="Quantity")
    currency_id: Optional[int] = Field(None, description="Currency details")
    income_price: float = Field(..., description="Income price")
    selling_price: float = Field(..., description="Selling price")
    currency_type_id: int = Field(..., description="Currency type")
    income_price_usd: Optional[float] = Field(None, description="Income price in USD")
    selling_percentage: Optional[float] = Field(None, description="Selling percentage")
    item_id: int = Field(..., description="Item details")


class BuyDocumentModelScheme(BaseModel):
    product_doc_items: List[DocumentItemModelScheme] = Field(
        ..., description="List of product document items"
    )


class DebtDataScheme(BaseModel):
    full_name: Optional[None] = Field(
        default=None,
        description="Customer's full name")
    phone_number: Optional[None] = Field(
        default=None,
        description="Customer's phone number")
    phone_number2: Optional[None] = Field(

        default=None, description="Customer's phone number"

    )
    address: Optional[None] = Field(description="Customer's address", default=None)
    amount: Optional[None] = Field(description="Debt amount", default=None)


class SellDocumentModelScheme(BaseModel):
    customer_id: Optional[int] = Field(description="Client's id")
    debt_data: DebtDataScheme = Field()
    is_debt: bool = Field()
    product_doc_items: List[DocumentItemModelScheme] = Field(
        ..., description="List of product document items"
    )


class DocumentItemBalanceUpdatedScheme(BaseModel):
    qty: Optional[int] = None
    income_price_usd: Optional[float] = None
    income_price: Optional[float] = None
    selling_price: Optional[float] = None
    selling_percentage: Optional[float] = None
