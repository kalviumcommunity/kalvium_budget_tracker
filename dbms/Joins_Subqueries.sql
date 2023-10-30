-- Update the MonthlyReport table's Total_Income for the user for that month
UPDATE MonthlyReport mr
JOIN (
    SELECT Email, SUM(Transaction_Amount) as TotalIncomeForMonth
    FROM Transaction
    WHERE Transaction_Type = 'Income' AND Email = 'test' AND MONTH(Transaction_Date) = 10 AND YEAR(Transaction_Date) = 2023
    GROUP BY Email
) AS temp ON mr.Email = temp.Email AND mr.Report_Month = '2023-10-01'
SET mr.Total_Income = temp.TotalIncomeForMonth
WHERE mr.Email = 'test' AND mr.Report_Month = '2023-10-01';


-- Update the MonthlyReport table's Total_Expense for the user for that month
UPDATE MonthlyReport mr
JOIN (
    SELECT Email, SUM(Transaction_Amount) as TotalExpenseForMonth
    FROM Transaction
    WHERE Transaction_Type = 'Expense' AND Email = 'test' AND MONTH(Transaction_Date) = 10 AND YEAR(Transaction_Date) = 2023
    GROUP BY Email
) AS temp ON mr.Email = temp.Email AND mr.Report_Month = '2023-10-01'
SET mr.Total_Expense = temp.TotalExpenseForMonth
WHERE mr.Email = 'test' AND mr.Report_Month = '2023-10-01';
