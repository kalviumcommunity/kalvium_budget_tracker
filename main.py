from fastapi import FastAPI
from api.endpoints import user, transaction

app = FastAPI(title="Kalvium Budget Tracker", description="A financial tracker application")

# Add the routers here
app.include_router(user.router)
app.include_router(transaction.router)
# app.include_router(investment.router)
