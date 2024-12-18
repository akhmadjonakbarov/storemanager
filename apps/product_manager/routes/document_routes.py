from fastapi import APIRouter, HTTPException
from starlette import status
from .db_writer.create_document import create_document
from .db_writer.manage_item import create_doc_item, create_doc_item_balance
from apps import DocumentModel, DocumentItemModel, DocumentItemBalanceModel
from di.db import db_dependency
from di.user import user_dependency
from utils.response_type import *
from ..schemes import DocumentModelScheme

router = APIRouter(
    prefix="/document",
    tags=["Documents CRUD"],
)


@router.get('/all')
async def get_documents(db: db_dependency):
    return db.query(DocumentModel).filter_by(is_deleted=False).all()


@router.post('/buy', status_code=status.HTTP_201_CREATED)
async def buy_document(db: db_dependency, user: user_dependency, document_scheme: DocumentModelScheme):
    try:
        with db.begin():
            # Step 1: Create the main document
            document: DocumentModel = create_document(user_id=user.get('id'))
            db.add(document)
            db.flush()  # Ensure the document gets an ID before proceeding
            db.refresh(document)  # Refresh to get the document ID

            # Step 2: Loop through product_doc_items and add them
            for item_scheme in document_scheme.product_doc_items:
                new_doc_item = create_doc_item(
                    element=item_scheme,
                    user_id=user.get('id'),
                    document_id=document.id  # Pass the correct document ID
                )
                db.add(new_doc_item)
                db.flush()  # Ensure the document item gets an ID before proceeding
                db.refresh(new_doc_item)  # Refresh to get the document_item_id

                # Step 3: Update or create balance for each item
                item_balance: DocumentItemBalanceModel = db.query(DocumentItemBalanceModel).filter_by(
                    item_id=item_scheme.item_id
                ).first()

                if not item_balance or item_balance.income_price != new_doc_item.income_price:
                    # Create a new balance and set document_item_id
                    new_balance = create_doc_item_balance(
                        user_id=user.get('id'),
                        doc_item=new_doc_item
                    )
                    db.add(new_balance)
                else:
                    # Update existing balance
                    item_balance.qty += new_doc_item.qty
                    item_balance.qty_kg += new_doc_item.qty_kg
                    item_balance.document_item_id = new_doc_item.id  # Ensure this is set

        return res_message(
            message=ResponseMessages.SUCCESS
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete('/delete/{doc_id}', status_code=status.HTTP_200_OK)
async def delete_document(db: db_dependency, user: user_dependency, doc_id: int):
    try:
        with db.begin():
            document: DocumentModel = db.query(DocumentModel).filter_by(id=doc_id).first()
            if not document:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=ResponseMessages.DATA_NOT_FOUND
                )
            document.soft_delete()
        return res_message(ResponseMessages.SUCCESS)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
