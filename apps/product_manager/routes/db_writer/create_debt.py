from apps.debt.models import DebtModel


def create_debt(
        full_name: str, phone_number: str, phone_number2: str,
        address: str, user_id: int, amount: float
) -> DebtModel:
    debt = DebtModel(
        name=full_name,
        phone_number=phone_number,
        phone_number2=phone_number2,
        address=address,
        user_id=user_id,
        amount=amount
    )

    return debt
