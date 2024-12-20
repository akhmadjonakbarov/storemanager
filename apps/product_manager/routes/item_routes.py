from fastapi import APIRouter, HTTPException
from apps.product_manager.models import ItemModel
from apps.product_manager.schemes import ItemScheme
from di.db import db_dependency
from di.user import user_dependency
from .serializers.common_serializers import ItemModelSerializer

router = APIRouter(
    prefix="/item",
    tags=["Item CRUD"],
)


@router.get("/all")
async def get_items(db: db_dependency):
    serializer = ItemModelSerializer(many=True)
    items = db.query(ItemModel).all()
    serialized_items = serializer.dump(items)
    return serialized_items


@router.post("/add")
async def add_item(db: db_dependency, user: user_dependency, item: ItemScheme):
    try:

        item = ItemModel(**item.dict(), user_id=user.get('id'))
        db.add(item)
        db.commit()
        return item
    except Exception as e:
        db.rollback()
        return HTTPException(
            status_code=400, detail=str(e)
        )
