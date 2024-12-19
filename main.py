import uvicorn
from fastapi import FastAPI
from apps.currency.routes import currency_type_routes
from apps.product_manager.routes import item_routes, unit_routes, category_routes, document_routes, store_routes
from apps.user import routes as user_routes
from apps.debt import routes as debt_routes
from config.database_config import engine
from apps.base.models import Base

app = FastAPI(
    title="Store Manager",
)
Base.metadata.create_all(bind=engine)

BASE_API_URL = "/api/v1"
app.include_router(user_routes.router, prefix=BASE_API_URL)
app.include_router(store_routes.router, prefix=BASE_API_URL)
app.include_router(item_routes.router, prefix=BASE_API_URL)
app.include_router(unit_routes.router, prefix=BASE_API_URL)
app.include_router(category_routes.router, prefix=BASE_API_URL)
app.include_router(document_routes.router, prefix=BASE_API_URL)
app.include_router(debt_routes.router, prefix=BASE_API_URL)
app.include_router(currency_type_routes.router, prefix=BASE_API_URL)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
