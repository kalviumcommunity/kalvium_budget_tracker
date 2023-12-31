from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

# Classes and objects
# Each of these classes represent a distinct entity in the application.

# User class representing a user in the system
class User(BaseModel):
    email: str
    fname: str
    sname: str
    hashed_password: str
    incomes: List = []
    expenses: List = []
    investments: List = []

    # Constructor
    def __init__(self, **data):
        super().__init__(**data)  # Calling the parent (BaseModel) constructor
        print(f"User {self.email} is being created")

    # Destructor
    def __del__(self):
        print(f"User {self.email} is being destroyed")

    # Method to calculate total income
    def get_total_income(self):
        print("Using 'self' to calculate total income for:", self.email)
        return sum(income.income_amount for income in self.incomes)

    # Method to calculate total expense
    def get_total_expense(self):
        print("Using 'self' to calculate total expense for:", self.email)
        return sum(expense.expense_amount for expense in self.expenses)

    # Method to calculate balance
    def get_balance(self):
        print("Using 'self' to calculate balance for:", self.email)
        return self.get_total_income() - self.get_total_expense()    

# Model for user registration
class RegisterUser(BaseModel):
    email: str
    password: str

# Income class representing an income entry for a user
class Income(BaseModel):
    income_date: datetime
    income_details: str
    income_amount: float

# Expense Category 
class ExpenseCategory(str, Enum):
    food = "Food"
    transport = "Transport"
    utilities = "Utilities"
    entertainment = "Entertainment"
    health = "Health"
    others = "Others"

# Expense class representing an expense entry for a user
class Expense(BaseModel):
    expense_date: datetime
    expense_details: str
    expense_amount: float
    expense_category: ExpenseCategory

# Investment Type
class InvestmentType(str, Enum):
    st = 'stock',
    mf = 'mutual fund'

# Investment class representing an investment entry for a user
class Investment(BaseModel):
    date_of_investment: datetime
    investment_category: str
    investment_symbol: str
    investment_amount: float
    investment_type: InvestmentType

# SavingsGoal class representing a savings goal for a user
class SavingsGoal(BaseModel):
    goal_amount: float
    current_amount: float
    target_date: datetime

# MonthlyReport class representing a monthly report for a user
class MonthlyReport(BaseModel):
    total_income: float
    total_expense: float
    total_investment: float
    total_savings: float


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str
