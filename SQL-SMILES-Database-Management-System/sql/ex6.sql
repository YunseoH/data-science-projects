-- ex6. sql
-- 1. Insert the result of the query
CREATE TABLE VIPClients (
    ClientNo INT PRIMARY KEY,
    fName VARCHAR(50),
    lName VARCHAR(50),
    Email VARCHAR(100),
    TotalRentals INT
);

INSERT INTO VIPClients (ClientNo, fName, lName, Email, TotalRentals)
SELECT C.ClientNo, C.fName, C.lName, C.Email, COUNT(H.HireNo) AS TotalRentals
FROM Client AS C
JOIN HireAgreement H ON C.ClientNo = H.ClientNo
GROUP BY C.ClientNo, C.fName, C.lName, C.Email
HAVING COUNT(H.HireNo) >= 3;  

SELECT * FROM VIPClients;

-- 2. Updating several tuples at once

-- Disable dafe update mode
SET SQL_SAFE_UPDATES = 0;

-- Query starts here
UPDATE Vehicle AS V
JOIN (
    SELECT VehicleRegNo, COUNT(*) AS RentalCount
    FROM HireAgreement
    GROUP BY VehicleRegNo
    HAVING COUNT(*) > 3
) AS FrequentRentals
ON V.RegistrationNo = FrequentRentals.VehicleRegNo
SET V.HireRate = ROUND(V.HireRate * 1.10, 2);

-- 3. Delete a Set of Tuples
DELETE FROM HireAgreement
WHERE VehicleRegNo IN (SELECT RegistrationNo FROM Vehicle WHERE Status != 'Available')
AND StartDate < '2023-01-01';
