from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from .base import Base
from enum import Enum
from pydantic import BaseModel

class TransactionType(Enum):
    Income = "Income"
    Expense = "Expense"

class UserDB(Base):
    __tablename__ = "users"

    email = Column(String, primary_key=True, index=True)
    fname = Column(String)
    sname = Column(String)
    hashed_password = Column(String)
    
    transactions = relationship("TransactionDB", back_populates="owner")
    investments = relationship("InvestmentDB", back_populates="owner")
    monthly_reports = relationship("MonthlyReport", back_populates="owner")


class IncomeCategoryDB(Base):
    __tablename__ = "IncomeCategory"
    
    Inc_Cat_ID = Column(Integer, primary_key=True, index=True)
    category_name = Column(String)
    transactions = relationship("TransactionDB", back_populates="income_category")

class ExpenseCategoryDB(Base):
    __tablename__ = "ExpenseCategory"
    
    Exp_Cat_ID = Column(Integer, primary_key=True, index=True)
    category_name = Column(String)
    transactions = relationship("TransactionDB", back_populates="expense_category")

class TransactionDB(Base):
    __tablename__ = "Transaction"

    Transaction_ID = Column(Integer, primary_key=True, index=True)
    Transaction_Date = Column(DateTime, index=True)
    Transaction_Details = Column(String)
    Transaction_Amount = Column(Float)
    Transaction_Type = Column(String, CheckConstraint("Transaction_Type IN ('Income', 'Expense')"))
    Email = Column(String, ForeignKey("users.email"))
    Income_Category_ID = Column(Integer, ForeignKey('IncomeCategory.Inc_Cat_ID'))
    Expense_Category_ID = Column(Integer, ForeignKey('ExpenseCategory.Exp_Cat_ID'))
    
    owner = relationship("UserDB", back_populates="transactions")
    income_category = relationship("IncomeCategoryDB", back_populates="transactions")
    expense_category = relationship("ExpenseCategoryDB", back_populates="transactions")

class InvestmentTypeDB(Base):
    __tablename__ = "InvestmentType"
    
    Inv_Type_ID = Column(Integer, primary_key=True, index=True)
    Inv_Type = Column(String, nullable=False)

    investments = relationship("InvestmentDB", back_populates="investment_type")

class InvestmentDB(Base):
    __tablename__ = "Investment"

    Investment_ID = Column(Integer, primary_key=True, index=True)
    Date_of_Investment = Column(DateTime, nullable=False)
    Inv_Symbol = Column(String, ForeignKey("InvestmentCompany.Inv_Symbol"))
    Investment_Amount = Column(Float, nullable=False)
    Investment_Type_ID = Column(Integer, ForeignKey("InvestmentType.Inv_Type_ID"))

    email = Column(String, ForeignKey("users.email"))
    owner = relationship("UserDB", back_populates="investments")
    investment_type = relationship("InvestmentTypeDB", back_populates="investments")

class MonthlyReport(Base):
    __tablename__ = "MonthlyReport"

    ID = Column(Integer, primary_key=True, index=True)
    Email = Column(String, ForeignKey("users.email"))
    Total_Income = Column(Float, nullable=False)
    Total_Expense = Column(Float, nullable=False)
    Total_Investment = Column(Float, nullable=False)

    owner = relationship("UserDB", back_populates="monthly_reports")
