INSERT INTO User (Email, FName, SName, Hashed_Password)
VALUES ('ary7sharma@gmail.com', 'Ary', 'Sharma', 'hashed_password');

UPDATE User 
SET FName = 'Aryan', SName = 'Sharma' 
WHERE Email = 'ary7sharma@gmail.com';

SELECT * FROM User;

INSERT INTO IncomeCategory (Inc_Cat_ID, Inc_Cat)
VALUES (1,  'Salary')

INSERT INTO ExpenseCategory (Exp_Cat_ID, Exp_Cat)
VALUES (1, 'Rent');

INSERT INTO InvestmentCompany (Inv_Symbol, Comp_Name)
VALUES ('AAPL', 'Apple Inc.');

INSERT INTO InvestmentType (Inv_Type_ID, Inv_Type)
VALUES (1, 'Stocks');

INSERT INTO Transaction (Transaction_ID, Email, Transaction_Date, Transaction_Details, Transaction_Amount, Transaction_Type, Income_Category_ID)
VALUES (1, 'ary7sharma@gmail.com', '2023-09-23', 'Monthly Salary', 25000.00, 'Income', 1);

DELETE FROM Transaction 
WHERE Transaction_ID = 1;

SELECT * FROM Transaction 
WHERE Email = 'ary7sharma@gmail.com';

INSERT INTO Investment (Investment_ID, Email, Date_of_Investment, Inv_Symbol, Investment_Amount, Investment_Type_ID)
VALUES (1, 'ary7sharma@gmail.com', '2023-09-24', 'AAPL', 3000.00, 1);

INSERT INTO SavingsGoal (ID, UserID, Goal_Amount, Current_Amount, Target_Date)
VALUES (1, 'ary7sharma@gmail.com', 10000.00, 2000.00, '2023-12-31');

