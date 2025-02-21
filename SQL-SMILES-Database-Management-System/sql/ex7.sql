-- ex7.sql: CREATE VIEW statements

-- View 1
CREATE OR REPLACE VIEW ActiveClients AS
SELECT 
    C.ClientNo, 
    C.fName, 
    C.lName, 
    C.Email, 
    H.VehicleRegNo, 
    H.StartDate, 
    H.TerminationDate
FROM Client C
JOIN HireAgreement H ON C.ClientNo = H.ClientNo
WHERE H.TerminationDate > (CURDATE() - INTERVAL 30 DAY);

-- View 2
CREATE OR REPLACE VIEW AvailableVehicles AS
SELECT 
    RegistrationNo, 
    PlateNo, 
    Type, 
    Model, 
    Make, 
    HireRate
FROM Vehicle
WHERE Status = 'Available';

-- View 3
CREATE OR REPLACE VIEW HighSpendingClients AS
SELECT 
    c.ClientNo, 
    c.fName, 
    c.lName, 
    SUM(h.TotalCost) AS TotalSpent
FROM Client c
JOIN HireAgreement h ON c.ClientNo = h.ClientNo
GROUP BY c.ClientNo
HAVING TotalSpent > 500; 

-- Running Queries on Views 
SELECT * FROM ActiveClients;
SELECT * FROM AvailableVehicles ORDER BY HireRate DESC;
SELECT * FROM HighSpendingClients;

--  Testing View Updatability
INSERT INTO ActiveClients (ClientNo, fName, lName, Email, VehicleRegNo, StartDate, TerminationDate)
VALUES (999, 'John', 'Doe', 'john.doe@email.com', 'V101', '2025-02-01', '2025-02-15');
-- The ActiveClients view is not updatable because it is based on a JOIN between multiple tables 
-- (Client and HireAgreement). MySQL does not allow inserting or updating data through 
-- views that modify more than one base table. Additionally, the view filters data using 
-- a WHERE condition, further restricting its updatability. Since an insert into this 
-- view would require adding records to both Client and HireAgreement, MySQL blocks the 
-- operation.

UPDATE AvailableVehicles SET HireRate = 200 WHERE RegistrationNo = 'V101';
-- The UPDATE AvailableVehicles statement did not cause an error, but it also did not 
-- modify any rows because the AvailableVehicles view is not fully updatable. The view 
-- filters rows using a WHERE condition (Status = 'Available'), meaning any row that 
-- gets updated in a way that changes its availability could disappear from the view. 
-- Additionally, the view does not include all columns from the Vehicle table, which 
-- MySQL requires for updates to work. Since V101 was not found in the view, MySQL did 
-- not apply any changes.

DELETE FROM HighSpendingClients WHERE ClientNo = 101;
-- The HighSpendingClients view is not updatable because it is based on an aggregate 
-- function (SUM(TotalCost)) and a GROUP BY clause. When a view aggregates data from 
-- multiple rows into a single row, MySQL cannot determine which base table rows should 
-- be deleted. Since DELETE operations require direct access to rows in a table, MySQL 
-- prevents deletion from this view.