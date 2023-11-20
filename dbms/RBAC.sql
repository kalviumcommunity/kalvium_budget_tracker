CREATE TABLE Role (
    Role_ID INT PRIMARY KEY,
    Role_Name VARCHAR(255) NOT NULL
);

CREATE TABLE RolePrivilege (
    RolePrivilege_ID INT PRIMARY KEY,
    Role_ID INT,
    Privilege_Name VARCHAR(255) NOT NULL,
    Table_Name VARCHAR(255) NOT NULL,
    Access_Type VARCHAR(255) CHECK (Access_Type IN ('SELECT', 'INSERT', 'UPDATE', 'DELETE')),
    FOREIGN KEY (Role_ID) REFERENCES Role(Role_ID)
);

CREATE TABLE UserRole (
    UserRole_ID INT PRIMARY KEY,
    Email VARCHAR(255),
    Role_ID INT,
    FOREIGN KEY (Email) REFERENCES Users(Email),
    FOREIGN KEY (Role_ID) REFERENCES Role(Role_ID)
);

CREATE ROLE 'Admin';
CREATE ROLE 'User';


-- Grant the 'admin' role all privileges on the database
GRANT ALL PRIVILEGES ON `kalvium_budget_tracker`.* TO 'Admin';

-- Grant the 'user' role SELECT and INSERT privileges on the 'Transaction' table
GRANT SELECT, INSERT ON `kalvium_budget_tracker`.`Transaction` TO 'aryan.sharma@kalvium.community'@'localhost'; 

GRANT 'Admin' TO 'test'@'localhost';
GRANT 'User' TO 'aryan.sharma@kalvium.community'@'localhost';

FLUSH PRIVILEGES;


DELIMITER //
CREATE TRIGGER before_transaction_insert BEFORE INSERT ON Transaction
FOR EACH ROW
BEGIN
  DECLARE user_role_name VARCHAR(255);

  -- Get the role of the user trying to perform the insert
  SELECT r.Role_Name INTO user_role_name
  FROM UserRole ur
  JOIN Role r ON ur.Role_ID = r.Role_ID
  WHERE ur.Email = NEW.Email;

  -- If the user role is not 'Admin', signal an error
  IF user_role_name != 'Admin' THEN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Role-based error: Only Admins can insert into Transaction table';
  END IF;
END;
//
DELIMITER ;

INSERT INTO Transaction (Transaction_ID, Email, Transaction_Date, Transaction_Details, Transaction_Amount, Transaction_Type, Income_Category_ID)
VALUES (8, 'aryan.sharma@kalvium.community', '2023-10-31', 'Test', 1000.00, 'Income', 1);


SELECT r.Role_Name
FROM UserRole ur
JOIN Role r ON ur.Role_ID = r.Role_ID
WHERE ur.Email = 'test';
