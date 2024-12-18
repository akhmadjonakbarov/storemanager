from typing import Annotated
from fastapi import Depends

from apps.user.utils.user_manager import get_current_user

user_dependency = Annotated[dict, Depends(get_current_user)]
