from fastapi import APIRouter
from starlette import status

from apps.product_manager.models import DocumentItemModel, DocumentModel
from di.db import db_dependency
from di.user import user_dependency
from utils.response_type import *

router = APIRouter(
    prefix="/doc-item",
    tags=["Document Item CRUD"],
)


@router.get("/all", status_code=status.HTTP_200_OK)
async def get_products(db: db_dependency, user: user_dependency, document_id=None):
    doc_items = db.query(DocumentItemModel).all()
    if document_id is not None:
        document: DocumentModel = db.query(DocumentModel).filter_by(id=document_id, is_deleted=False).first()
        if document is not None:
            doc_items = db.query(DocumentItemModel).filter_by(document_id=document.id).all()
    return response_list(lst=doc_items)
