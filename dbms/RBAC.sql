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

-- Adding roles
INSERT INTO Role (Role_ID, Role_Name) VALUES (1, 'Admin');
INSERT INTO Role (Role_ID, Role_Name) VALUES (2, 'User');

-- Adding privileges
INSERT INTO RolePrivilege (RolePrivilege_ID, Role_ID, Privilege_Name, Table_Name, Access_Type) VALUES (1, 1, 'Manage Users', 'Users', 'SELECT');
INSERT INTO RolePrivilege (RolePrivilege_ID, Role_ID, Privilege_Name, Table_Name, Access_Type) VALUES (2, 1, 'Manage Users', 'Users', 'INSERT');

INSERT INTO UserRole (UserRole_ID, Email, Role_ID) VALUES (1, 'test', 1);
INSERT INTO UserRole (UserRole_ID, Email, Role_ID) VALUES (2, 'aryan.sharma@kalvium.community', 2);



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
WHERE ur.Email = 'aryan.sharma@kalvium.community';
