from fastapi import APIRouter, HTTPException, status

from apps.currency.models import CurrencyTypeModel
from apps.currency.schemes import CurrencyTypeScheme
from di.db import db_dependency
from utils.response_type import response_list

router = APIRouter(
    prefix="/currency-types",
    tags=["Currency Types"],
)


# 1. Get all currency types
@router.get("/all", status_code=status.HTTP_200_OK)
async def get_currency_types(db: db_dependency):
    try:
        currency_types = db.query(CurrencyTypeModel).all()
        return response_list(
            lst=currency_types
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# 2. Add a new currency type
@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_currency_type(
        currency_scheme: CurrencyTypeScheme,
        db: db_dependency
):
    new_currency = None
    try:

        with db.begin():
            new_currency = CurrencyTypeModel(name=currency_scheme.name)
            db.add(new_currency)
        db.refresh(new_currency)
        return new_currency
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


# 3. Update an existing currency type
@router.patch("/update/{currency_id}")
async def update_currency_type(
        db: db_dependency,
        currency_id: int,
        currency_scheme: CurrencyTypeScheme,
):
    currency = get_currency_or_404(db, currency_id)
    currency.name = currency_scheme.name
    db.commit()
    db.refresh(currency)
    return currency


# 4. Soft delete a currency type
@router.delete("/delete/{currency_id}", status_code=status.HTTP_200_OK)
async def delete_currency_type(currency_id: int, db: db_dependency):
    try:
        currency = get_currency_or_404(db, currency_id)
        currency.soft_delete()
        db.refresh(currency)
        return {"message": "Currency type deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


def get_currency_or_404(db: db_dependency, currency_id: int) -> CurrencyTypeModel:
    currency = db.query(CurrencyTypeModel).filter_by(id=currency_id).first()
    if not currency:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Currency type not found"
        )
    return currency
