from fastapi import APIRouter, Depends, HTTPException
from database.models import MonthlyReport
from sqlalchemy.orm import Session
from database.schemas import Transaction, User, BatchTransactions
from api.dependencies import get_db, get_user, get_current_user
from sqlalchemy.sql.expression import extract
from ..transaction_processors import IncomeTransactionProcessor, ExpenseTransactionProcessor
from database.models import MonthlyReport
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
    processor = None
    if transaction.Transaction_Type == 'Income':
        processor = IncomeTransactionProcessor()
    elif transaction.Transaction_Type == 'Expense':
        processor = ExpenseTransactionProcessor()

    if processor:
        current_month = transaction.Transaction_Date.month
        current_year = transaction.Transaction_Date.year

        report = db.query(MonthlyReport).filter(
            MonthlyReport.Email == current_user.email
        ).filter(
            extract('month', transaction.Transaction_Date) == current_month,
            extract('year', transaction.Transaction_Date) == current_year
        ).first()

        if not report:
            report = MonthlyReport(Email=current_user.email, Total_Income=0, Total_Expense=0, Total_Investment=0)
            db.add(report)
            db.commit()

        processor.process_transaction(transaction, db)
