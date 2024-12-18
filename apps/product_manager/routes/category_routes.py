from fastapi import APIRouter, HTTPException
from starlette import status
from utils.response_type import *
from apps.product_manager.models import CategoryModel
from apps.product_manager.schemes import CategoryScheme
from di.db import db_dependency

router = APIRouter(
    prefix="/category",
    tags=["Category CRUD"],
)


@router.get('/all', status_code=status.HTTP_200_OK)
async def get_categories(db: db_dependency):
    categories = db.query(CategoryModel).filter_by(is_deleted=False).all()
    return response_list(lst=categories)


@router.post('/add', status_code=status.HTTP_201_CREATED)
async def add_category(
        db: db_dependency,
        category_scheme: CategoryScheme
):
    try:
        category = CategoryModel(**category_scheme.dict())
        db.add(category)
        db.commit()
        return response_item(category)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch('/update/{category_id}')
async def update_category(
        db: db_dependency,
        category_id: int,
        category_scheme: CategoryScheme
):
    try:
        category = db.query(CategoryModel).filter_by(id=category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        category.full_name = category_scheme.name
        db.commit()
        return category
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete('/delete/{category_id}', status_code=status.HTTP_200_OK)
async def delete_category(db: db_dependency, category_id: int):
    try:
        category: CategoryModel = db.query(CategoryModel).filter_by(id=category_id).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found"
            )
        category.soft_delete()
        db.commit()
        return {"message": "Category deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
