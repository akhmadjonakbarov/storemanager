from apps import DocumentModel


def create_document(user_id, is_sell: bool = False) -> DocumentModel:
    document = DocumentModel(
        doc_type=DocumentModel.SELL if is_sell else DocumentModel.BUY,
        user_id=user_id
    )
    return document
