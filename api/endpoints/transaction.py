from fastapi import APIRouter, Depends, HTTPException
from database.models import TransactionType, MonthlyReport, TransactionDB, IncomeCategoryDB, ExpenseCategoryDB
from sqlalchemy.orm import Session
from database.schemas import Transaction, User, BatchTransactions
from api.dependencies import get_db, get_user, get_current_user
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

        if transaction.Transaction_Type == 'Income':
            income_category = db.query(IncomeCategoryDB).filter(IncomeCategoryDB.Inc_Cat_ID == transaction.Income_Category_ID).first()
            if not income_category:
                raise HTTPException(status_code=400, detail="Income category not found")
            # Update MonthlyReport with income
            db.query(MonthlyReport).filter(MonthlyReport.Email == current_user.email).update({
                MonthlyReport.Total_Income: MonthlyReport.Total_Income + transaction.Transaction_Amount
            })
        elif transaction.Transaction_Type == 'Expense':
            expense_category = db.query(ExpenseCategoryDB).filter(ExpenseCategoryDB.Exp_Cat_ID == transaction.Expense_Category_ID).first()
            if not expense_category:
                raise HTTPException(status_code=400, detail="Expense category not found")
            # Update MonthlyReport with expense
            db.query(MonthlyReport).filter(MonthlyReport.Email == current_user.email).update({
                MonthlyReport.Total_Expense: MonthlyReport.Total_Expense + transaction.Transaction_Amount
            })

        db.commit()

        transaction_data = transaction.dict()

        db_transaction = TransactionDB(**transaction_data, owner=db_user)
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return {"msg": "Transaction added successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")
