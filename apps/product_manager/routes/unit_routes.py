from fastapi import APIRouter, HTTPException
from starlette import status

from apps.product_manager.models import UnitModel
from apps.product_manager.schemes import UnitScheme
from di.db import db_dependency
from di.user import user_dependency

router = APIRouter(
    prefix="/unit",
    tags=["Unit CRUD"],
)


@router.get('/all', status_code=status.HTTP_200_OK)
async def get_units(db: db_dependency):
    return db.query(UnitModel).all()


@router.post('/add', status_code=status.HTTP_201_CREATED)
async def add_unit(db: db_dependency, unit_body: UnitScheme):
    try:
        unit = UnitModel(**unit_body.dict())
        db.add(unit)
        db.commit()
        db.refresh(unit)
        return unit
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=str(e)
        )


@router.patch('/update/{unit_id}', status_code=status.HTTP_200_OK)
async def update_unit(db: db_dependency, unit_id: int, unit_scheme: UnitScheme):
    try:
        unit: UnitModel = db.query(UnitModel).filter_by(id=unit_id).first()
        if not unit:
            raise HTTPException(status_code=404, detail="Unit not found")
        unit.value = unit_scheme.value
        db.commit()
        return unit
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=str(e)
        )


@router.delete('/delete/{unit_id}', status_code=status.HTTP_200_OK)
async def delete_unit(db: db_dependency, unit_id: int):
    try:
        unit: UnitModel = db.query(UnitModel).filter_by(id=unit_id).first()
        if not unit:
            raise HTTPException(status_code=404, detail="Unit not found")
        deleted_unit = unit.soft_delete()
        db.delete(deleted_unit)
        db.commit()
        return {"message": "Unit deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400, detail=str(e)
        )
