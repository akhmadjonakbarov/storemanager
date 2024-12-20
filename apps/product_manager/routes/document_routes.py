from fastapi import APIRouter, HTTPException
from starlette import status

from .db_writer.create_debt import create_debt
from .db_writer.create_document import create_document
from .db_writer.manage_item import create_doc_item, create_doc_item_balance
from apps import DocumentModel, DocumentItemBalanceModel
from di.db import db_dependency
from di.user import user_dependency
from utils.response_type import *
from apps.product_manager.schemes import *
from ...customer.models import CustomerModel
from .serializers.document_serializers import DocumentModelSerializer

router = APIRouter(
    prefix="/document",
    tags=["Documents CRUD"],
)


@router.get('/all')
async def get_documents(db: db_dependency):
    serializer = DocumentModelSerializer(many=True)
    documents = db.query(DocumentModel).filter_by(is_deleted=False).all()
    return response_list(lst=serializer.dump(documents))


@router.post('/buy', status_code=status.HTTP_201_CREATED)
async def buy_document(db: db_dependency, user: user_dependency, document_scheme: BuyDocumentModelScheme):
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


@router.post('/sell', status_code=status.HTTP_201_CREATED)
async def sell_document(db: db_dependency, user: user_dependency, document_scheme: SellDocumentModelScheme):
    try:
        with db.begin():
            new_document: DocumentModel = create_document(user_id=user.get('id'), is_sell=True)
            db.add(new_document)
            db.flush()  # Ensure the document gets an ID before proceeding
            db.refresh(new_document)  # Refresh to get the document ID
            if document_scheme.is_debt:
                if document_scheme.customer_id != -1:
                    customer = db.query(CustomerModel).filter_by(id=document_scheme.customer_id).first()
                    if not customer:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail="Customer not found"
                        )
                    else:
                        # create debt for customer
                        pass
                if document_scheme.debt_data.full_name is not None:
                    create_debt(
                        user_id=user.get('id'),
                        full_name=document_scheme.debt_data.full_name,
                        phone_number=document_scheme.debt_data.phone_number,
                        phone_number2=document_scheme.debt_data.phone_number2,
                        amount=document_scheme.debt_data.amount,
                        address=document_scheme.debt_data.address,
                    )
            else:
                if document_scheme.customer_id != -1:
                    customer: CustomerModel = db.query(CustomerModel).filter_by(id=document_scheme.customer_id).first()
                    if not customer:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail="Customer not found"
                        )
                    else:
                        new_document.customer_id = customer.id

            for item in range(len(document_scheme.product_doc_items)):
                item_data = document_scheme.product_doc_items[item]
                new_doc_item = create_doc_item(
                    element=item_data,
                    user_id=user.get('id'),
                    document_id=new_document.id  # Pass the correct document ID
                )
                db.add(new_doc_item)
                item_balance: DocumentItemBalanceModel = db.query(DocumentItemBalanceModel).filter_by(
                    item_id=item_data.item_id
                ).first()
                if item_balance:
                    total_qty = item_balance.qty - item_data.qty
                    if total_qty >= 0:
                        item_balance.qty = total_qty
                else:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=ResponseMessages.DATA_NOT_FOUND
                    )
        return res_message(
            ResponseMessages.SUCCESS
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


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
