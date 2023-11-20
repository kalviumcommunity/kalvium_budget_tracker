from fastapi import APIRouter, Depends, HTTPException
from database.models import TransactionType, MonthlyReport, TransactionDB, IncomeCategoryDB, ExpenseCategoryDB
from sqlalchemy.orm import Session
from database.schemas import Transaction, User, BatchTransactions
from api.dependencies import get_db, get_user, get_current_user
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import extract

router = APIRouter()

@router.post("/add_batch_transactions")
def add_batch_transactions(batch: BatchTransactions, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_user = get_user(db, current_user.email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for transaction in batch.transactions:
        process_single_transaction(transaction, current_user, db)
    return {"msg": "Batch transactions added successfully"}

def process_single_transaction(transaction: Transaction, current_user: User, db: Session):
    db_user = get_user(db, current_user.email)
    if db_user:
        current_month = transaction.Transaction_Date.month
        current_year = transaction.Transaction_Date.year
        report_month = transaction.Transaction_Date.replace(day=1)  # First day of the month

        # Fetch or create the MonthlyReport record
        report = db.query(MonthlyReport).filter(
            MonthlyReport.Email == current_user.email,
            extract('month', transaction.Transaction_Date) == current_month,
            extract('year', transaction.Transaction_Date) == current_year
        ).first()

        if not report:
            report = MonthlyReport(Email=current_user.email, Total_Income=0, Total_Expense=0, Total_Investment=0)
            db.add(report)
            db.commit()

        # Recalculate and update the MonthlyReport record
        total_income = db.query(func.sum(TransactionDB.Transaction_Amount)).filter(
            TransactionDB.Email == current_user.email,
            TransactionDB.Transaction_Type == 'Income',
            extract('month', TransactionDB.Transaction_Date) == current_month,
            extract('year', TransactionDB.Transaction_Date) == current_year
        ).scalar() or 0

        total_expense = db.query(func.sum(TransactionDB.Transaction_Amount)).filter(
            TransactionDB.Email == current_user.email,
            TransactionDB.Transaction_Type == 'Expense',
            extract('month', TransactionDB.Transaction_Date) == current_month,
            extract('year', TransactionDB.Transaction_Date) == current_year
        ).scalar() or 0

        report.Total_Income = total_income
        report.Total_Expense = total_expense
        
        db.commit()

        # Add the transaction to the Transaction table
        transaction_data = transaction.dict()
        db_transaction = TransactionDB(**transaction_data, owner=db_user)
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return {"msg": "Transaction added successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")
