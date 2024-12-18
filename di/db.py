from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

from config.database_config import db_init

db_dependency = Annotated[Session, Depends(db_init)]
