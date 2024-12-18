from fastapi import APIRouter, HTTPException
from starlette import status

from apps.debt.models import DebtModel
from apps.debt.schemes import DebtScheme
from di.db import db_dependency
from di.user import user_dependency
from utils.response_type import response_list, response_item

router = APIRouter(
    prefix="/debt",
    tags=["Debt CRUD"],
)


@router.get('/all', status_code=status.HTTP_200_OK)
async def get_debts(db: db_dependency, user: user_dependency):
    debts = []
    try:
        with db.begin():
            debts = db.query(DebtModel).filter_by(is_paid=False, is_deleted=False).all()
        return response_list(
            lst=debts,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_debt(
        db: db_dependency, user: user_dependency, debt_scheme: DebtScheme
):
    new_debt = None
    try:
        with db.begin():
            new_debt = DebtModel(debt_scheme.dict(), user_id=user.get('id'))
            db.add(new_debt)
        db.refresh(new_debt)
        return response_item(
            item=new_debt
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
