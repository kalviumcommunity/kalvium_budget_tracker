-- Active: 1696396214334@@127.0.0.1@3306@kalvium_budget_tracker
CREATE TABLE User (
    Email VARCHAR(255) PRIMARY KEY,
    FName VARCHAR(255) NOT NULL,
    SName VARCHAR(255) NOT NULL
);

ALTER TABLE User ADD Hashed_Password VARCHAR(255) NOT NULL;

CREATE TABLE IncomeCategory (
    Inc_Cat_ID INT PRIMARY KEY,
    Inc_Cat VARCHAR(255) NOT NULL
);

CREATE TABLE ExpenseCategory (
    Exp_Cat_ID INT PRIMARY KEY,
    Exp_Cat VARCHAR(255) NOT NULL
);

CREATE TABLE InvestmentCompany (
    Inv_Symbol VARCHAR(255) PRIMARY KEY,
    Comp_Name VARCHAR(255) NOT NULL
);

CREATE TABLE InvestmentType (
    Inv_Type_ID INT PRIMARY KEY,
    Inv_Type VARCHAR(255) NOT NULL
);

CREATE TABLE Transaction (
    Transaction_ID INT PRIMARY KEY,
    Email VARCHAR(255) REFERENCES User(Email),
    Transaction_Date DATE NOT NULL,
    Transaction_Details VARCHAR(255),
    Transaction_Amount FLOAT NOT NULL,
    Transaction_Type VARCHAR(255) CHECK (Transaction_Type IN ('Income', 'Expense')),
    Income_Category_ID INT REFERENCES IncomeCategory(Inc_Cat_ID),
    Expense_Category_ID INT REFERENCES ExpenseCategory(Exp_Cat_ID)
);

CREATE TABLE Investment (
    Investment_ID INT PRIMARY KEY,
    Email VARCHAR(255) REFERENCES User(Email),
    Date_of_Investment DATE NOT NULL,
    Inv_Symbol VARCHAR(255) REFERENCES InvestmentCompany(Inv_Symbol),
    Investment_Amount FLOAT NOT NULL,
    Investment_Type_ID INT REFERENCES InvestmentType(Inv_Type_ID)
);

CREATE TABLE SavingsGoal (
    ID INT PRIMARY KEY,
    UserID VARCHAR(255) REFERENCES User(Email),
    Goal_Amount FLOAT NOT NULL,
    Current_Amount FLOAT NOT NULL,
    Target_Date DATE
);

CREATE TABLE MonthlyReport (
    ID INT PRIMARY KEY,
    Email VARCHAR(255) REFERENCES User(Email),
    Total_Income FLOAT NOT NULL,
    Total_Expense FLOAT NOT NULL,
    Total_Investment FLOAT NOT NULL,
    Total_Savings FLOAT NOT NULL
);

DROP TABLE MonthlyReport 