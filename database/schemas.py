from pydantic import BaseModel
from typing import Optional
import datetime
from typing import List

class RegisterUser(BaseModel):
    email: str
    password: str
    fname: str
    sname: str

class User(BaseModel):
    email: str
    fname: str
    sname: str

class Transaction(BaseModel):
    Transaction_ID: Optional[int] 
    Transaction_Date: datetime.datetime
    Transaction_Details: str
    Transaction_Amount: float
    Transaction_Type: str
    Email: str
    Income_Category_ID: Optional[int]
    Expense_Category_ID: Optional[int]

class BatchTransactions(BaseModel):
    transactions: List[Transaction]
