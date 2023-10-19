-- Active: 1696396214334@@127.0.0.1@3306@kalvium_budget_tracker
CREATE TABLE User (
    Email VARCHAR(255) PRIMARY KEY,
    FName VARCHAR(255) NOT NULL,
    SName VARCHAR(255) NOT NULL
);

ALTER TABLE User ADD Hashed_Password VARCHAR(255) NOT NULL;

RENAME TABLE user TO users;


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
    Email VARCHAR(255),
    Transaction_Date DATE NOT NULL,
    Transaction_Details VARCHAR(255),
    Transaction_Amount FLOAT NOT NULL,
    Transaction_Type VARCHAR(255) CHECK (Transaction_Type IN ('Income', 'Expense')),
    Income_Category_ID INT,
    Expense_Category_ID INT,
    FOREIGN KEY (Email) REFERENCES User(Email),
    FOREIGN KEY (Income_Category_ID) REFERENCES IncomeCategory(Inc_Cat_ID),
    FOREIGN KEY (Expense_Category_ID) REFERENCES ExpenseCategory(Exp_Cat_ID)
);


CREATE TABLE Investment (
    Investment_ID INT PRIMARY KEY,
    Email VARCHAR(255),
    Date_of_Investment DATE NOT NULL,
    Inv_Symbol VARCHAR(255),
    Investment_Amount FLOAT NOT NULL,
    Investment_Type_ID INT,
    FOREIGN KEY (Email) REFERENCES User(Email),
    FOREIGN KEY (Inv_Symbol) REFERENCES InvestmentCompany(Inv_Symbol),
    FOREIGN KEY (Investment_Type_ID) REFERENCES InvestmentType(Inv_Type_ID)
);

CREATE TABLE SavingsGoal (
    ID INT PRIMARY KEY,
    UserID VARCHAR(255),
    Goal_Amount FLOAT NOT NULL,
    Current_Amount FLOAT NOT NULL,
    Target_Date DATE,
    FOREIGN KEY (UserID) REFERENCES User(Email)
);

CREATE TABLE MonthlyReport (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Email VARCHAR(255),
    Total_Income FLOAT NOT NULL,
    Total_Expense FLOAT NOT NULL,
    Total_Investment FLOAT NOT NULL,
    FOREIGN KEY (Email) REFERENCES Users(Email)
);
DROP TABLE MonthlyReport 

