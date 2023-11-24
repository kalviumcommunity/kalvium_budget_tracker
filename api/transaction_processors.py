from abc import ABC, abstractmethod
from database.schemas import Transaction
from sqlalchemy.orm import Session
from fastapi import HTTPException
from database.models import MonthlyReport, IncomeCategoryDB, ExpenseCategoryDB
from sqlalchemy.sql.expression import extract

class TransactionProcessor(ABC):
    @abstractmethod
    def process_transaction(self, transaction: Transaction, db: Session):
        pass

class IncomeTransactionProcessor(TransactionProcessor):
    def process_transaction(self, transaction: Transaction, db: Session):
        print("Processing income transaction with the help of Interface...")
        income_category = db.query(IncomeCategoryDB).filter(IncomeCategoryDB.Inc_Cat_ID == transaction.Income_Category_ID).first()
        if not income_category:
            raise HTTPException(status_code=400, detail="Income category not found")
        # Update MonthlyReport with income
        db.query(MonthlyReport).filter(MonthlyReport.Email == transaction.Email).update({
            MonthlyReport.Total_Income: MonthlyReport.Total_Income + transaction.Transaction_Amount
        })
        db.commit()

class ExpenseTransactionProcessor(TransactionProcessor):
    def process_transaction(self, transaction: Transaction, db: Session):
        print("Processing expense transaction with the help of Interface...")
        expense_category = db.query(ExpenseCategoryDB).filter(ExpenseCategoryDB.Exp_Cat_ID == transaction.Expense_Category_ID).first()
        if not expense_category:
            raise HTTPException(status_code=400, detail="Expense category not found")
        # Update MonthlyReport with expense
        db.query(MonthlyReport).filter(MonthlyReport.Email == transaction.Email).update({
            MonthlyReport.Total_Expense: MonthlyReport.Total_Expense + transaction.Transaction_Amount
        })
        db.commit()