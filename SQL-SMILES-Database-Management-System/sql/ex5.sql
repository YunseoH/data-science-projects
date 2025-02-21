-- ex5.sql: SELECT-FROM-WHERE
-- 1. Basic form
SELECT RegistrationNo, PlateNo, Type, FuelType, Model, Make, HireRate
FROM Vehicle
WHERE Status = 'Available'
LIMIT 10;

-- 2. Subquery in WHERE command
SELECT V.RegistrationNo, V.Model, V.Make, V.Status
FROM Vehicle AS V
WHERE V.RegistrationNo NOT IN (SELECT DISTINCT VehicleRegNo FROM HireAgreement)
LIMIT 5;

-- 3. Join multiple tables
SELECT H.HireNo, C.fName, C.lName, V.Model, V.Make, H.StartDate, H.TerminationDate, H.TotalCost
FROM HireAgreement AS H
INNER JOIN Client AS C ON H.ClientNo = C.ClientNo
INNER JOIN Vehicle AS V ON H.VehicleRegNo = V.RegistrationNo
LIMIT 10;

-- 4. Exist
SELECT C.ClientNo, C.fName, C.lName, C.Email
FROM Client AS C
WHERE EXISTS (SELECT 1 FROM HireAgreement AS H WHERE H.ClientNo = C.ClientNo)
LIMIT 5;

-- 5. Group by & Having
SELECT V.RegistrationNo, V.PlateNo, V.Type, COUNT(H.VehicleRegNo) AS HireCount
FROM HireAgreement AS H
JOIN Vehicle AS V ON H.VehicleRegNo = V.RegistrationNo
GROUP BY V.RegistrationNo, V.PlateNo, V.Type
HAVING COUNT(H.VehicleRegNo) >= 3;

-- 6. Join and ORDER BY
SELECT C.ClientNo, C.fName, C.lName, SUM(H.TotalCost) AS TotalSpent
FROM Client AS C
JOIN HireAgreement AS H ON C.ClientNo = H.ClientNo
GROUP BY C.ClientNo, C.fName, C.lName
ORDER BY TotalSpent DESC
LIMIT 5;