INSERT INTO Users (Email, FName, SName, Hashed_Password)
VALUES ('aryan.sharma@kalvium.community', 'Aryan', 'Sharma', 'password');

UPDATE Users
SET FName = 'Ary', SName = 'Diesel' 
WHERE Email = 'aryan.sharma@kalvium.community';

SELECT * FROM Users;

INSERT INTO IncomeCategory (Inc_Cat_ID, Inc_Cat)
VALUES (2,  'Salary')

INSERT INTO ExpenseCategory (Exp_Cat_ID, Exp_Cat)
VALUES (2, 'Rent');

INSERT INTO InvestmentCompany (Inv_Symbol, Comp_Name)
VALUES ('GOOGL', 'Google');

INSERT INTO InvestmentType (Inv_Type_ID, Inv_Type)
VALUES (2, 'Stocks');

INSERT INTO Transaction (Transaction_ID, Email, Transaction_Date, Transaction_Details, Transaction_Amount, Transaction_Type, Income_Category_ID)
VALUES (5, 'aryan.sharma@kalvium.community', '2023-10-19', 'Protein Powder', 8000.00, 'Expense', 1);

DELETE FROM Transaction 
WHERE Transaction_ID = 5;

SELECT * FROM Transaction 
WHERE Email = 'aryan.sharma@kalvium.community';

INSERT INTO Investment (Investment_ID, Email, Date_of_Investment, Inv_Symbol, Investment_Amount, Investment_Type_ID)
VALUES (2, 'aryan.sharma@kalvium.community', '2023-10-19', 'GOOGL', 8000.00, 1);

INSERT INTO SavingsGoal (ID, UserID, Goal_Amount, Current_Amount, Target_Date)
VALUES (2, 'aryan.sharma@kalvium.community', 20000.00, 3000.00, '2023-12-31');

