from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from models import User, RegisterUser, Income, Expense, Investment, Token

app = FastAPI(title="Kalvium Budget Tracker", description="A financial tracker application")

SECRET_KEY = "secret_key_for_jwt"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Use a dictionary to store users with email as the key
users_db = {}

def get_user(email: str):
    return users_db.get(email)

def authenticate_user(email: str, password: str):
    # Using the User object stored in users_db dictionary
    user = get_user(email)
    if user and pwd_context.verify(password, user.hashed_password):
        return user
    return None

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(email)
    if user is None:
        raise credentials_exception
    return user

@app.post("/register", response_model=User)
def register(user: RegisterUser):
    # Creating a new User object
    hashed_password = pwd_context.hash(user.password)
    new_user = User(email=user.email, fname="", sname="", hashed_password=hashed_password)
    users_db[user.email] = new_user
    return new_user

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # Using the User object for authentication
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
     # Returning a Token object
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/add_income")
async def add_income(income: Income, current_user: User = Depends(get_current_user)):
    # Working with the Income object
    current_user.incomes.append(income)
    return {"msg": "Income added successfully"}

@app.post("/add_expense")
async def add_expense(expense: Expense, current_user: User = Depends(get_current_user)):
    # Working with the Expense object
    current_user.expenses.append(expense)
    return {"msg": "Expense added successfully"}

@app.post("/add_investment")
async def add_investment(investment: Investment, current_user: User = Depends(get_current_user)):
    # Working with the Investment object
    current_user.investments.append(investment)
    return {"msg": "Investment added successfully"}

@app.get("/user_details")
async def get_user_details(current_user: User = Depends(get_current_user)):
    # Using objects and their properties to calculate totals
    total_income = sum(income.income_amount for income in current_user.incomes)
    total_expense = sum(expense.expense_amount for expense in current_user.expenses)
    
    return {
        "email": current_user.email,
        "incomes": [income.dict() for income in current_user.incomes],
        "total_income": total_income,
        "expenses": [expense.dict() for expense in current_user.expenses],
        "total_expense": total_expense,
        "balance": total_income - total_expense,
        "investments": [investment.dict() for investment in current_user.investments]
    }
