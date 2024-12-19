from fastapi import APIRouter, HTTPException
from starlette import status

from apps.debt.models import DebtModel
from apps.debt.schemes import DebtScheme
from di.db import db_dependency
from di.user import user_dependency
from utils.response_messages import ResponseMessages
from utils.response_type import response_list, response_item, res_message

router = APIRouter(
    prefix="/debt",
    tags=["Debt CRUD"],
)


@router.get('/all', status_code=status.HTTP_200_OK)
async def get_debts(db: db_dependency, user: user_dependency):
    try:
        debts = db.query(DebtModel).filter_by(is_paid=False, is_deleted=False).all()
        return response_list(lst=debts)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_debt(
        db: db_dependency, user: user_dependency, debt_scheme: DebtScheme
):
    new_debt = None
    try:
        with db.begin():
            new_debt = DebtModel(
                full_name=debt_scheme.full_name, phone_number=debt_scheme.phone_number,
                phone_number2=debt_scheme.phone_number2, amount=debt_scheme.amount, address=debt_scheme.address,
                user_id=user.get('id')
            )
            db.add(new_debt)
        db.refresh(new_debt)
        return response_item(
            item=new_debt
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.patch("/pay/{debt_id}")
async def pay_debt(db: db_dependency, debt_id: int):
    debt = None
    try:
        with db.begin():
            debt = db.query(DebtModel).filter_by(id=debt_id).first()
            if not debt:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Debt not found")
            debt.is_paid = True
        db.refresh(debt)
        return response_item(
            item=debt
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/delete/{debt_id}")
async def delete_debt(db: db_dependency, debt_id):
    try:
        with db.begin():
            debt: DebtModel = db.query(DebtModel).filter_by(id=debt_id).first()
            if not debt:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Debt not found")
            debt.soft_delete()
        return res_message(message=ResponseMessages.SUCCESS)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
