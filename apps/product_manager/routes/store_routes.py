from fastapi import APIRouter, HTTPException
from starlette import status

from apps.product_manager.models import DocumentItemBalanceModel
from apps.product_manager.schemes import DocumentItemBalanceUpdatedScheme
from di.db import db_dependency
from di.user import user_dependency
from utils.response_type import *

router = APIRouter(
    prefix="/store",
    tags=["Store CRUD"],
)


@router.get("/all", status_code=status.HTTP_200_OK)
async def get_products_in_store(db: db_dependency, user: user_dependency):
    item_balances = db.query(DocumentItemBalanceModel).all()
    return response_list(lst=item_balances)


@router.patch("/update-item-balance/{item_balance_id}", status_code=status.HTTP_200_OK)
async def update_item_balance(
        db: db_dependency, user: user_dependency,
        item_scheme: DocumentItemBalanceUpdatedScheme,
        item_balance_id: int
):
    try:
        with db.begin():
            # Fetch the item balance and item
            item_balance = db.query(DocumentItemBalanceModel).filter_by(id=item_balance_id).first()
            if not item_balance:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item balance not found")

            item = item_balance.item  # Assuming the relationship is defined

            # Update fields with values from the request body
            if item_scheme.qty is not None:
                item_balance.qty = item_scheme.qty
                item.qty = item_scheme.qty
            if item_scheme.selling_price is not None:
                item_balance.selling_price = item_scheme.selling_price
                item.selling_price = item_scheme.selling_price
            if item_scheme.selling_percentage is not None:
                item_balance.selling_percentage = item_scheme.selling_percentage
                item.selling_percentage = item_scheme.selling_percentage

            # Return the updated item balance data
            return response_item(item_balance)

    except Exception as e:
        db.rollback()  # Rollback in case of an error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )
