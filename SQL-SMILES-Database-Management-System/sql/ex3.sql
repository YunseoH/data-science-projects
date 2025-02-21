-- ex3.sql: INSERT commands
-- 1. Basic INSERT
INSERT INTO Staff (fName, lName, Address, PhoneNo, DOB, Sex, NIN, DateJoined, JobTitle, Salary)
VALUES ('Yunseo', 'Heo', '28 College Ave West', '98129770', '2002-04-26', 
         'F', 'NIN12345', '2021-08-17', 'Associate', 50000.00);

SELECT * FROM Staff;

-- 2. INSERT Based on Existing Data
INSERT INTO Staff (fName, lName, Address, PhoneNo, DOB, Sex, NIN, DateJoined, JobTitle, Salary)
SELECT 'Julie', 'Lee',  Address, PhoneNo, DOB, Sex, 'NIN12346', '2022-10-30', 'Manager', Salary * 1.5 
FROM Staff
WHERE NIN = 'NIN12345';

SELECT * FROM Staff;

-- 3. Insert a Fault Report for Vehicles with High Mileage
INSERT INTO FaultReport (VehicleRegNo, StaffNo, ReportDate, FaultDescription, FaultFound)
SELECT v.RegistrationNo, 1, '2025-02-15', 'Automatic Inspection Required: High mileage vehicle', 'Y'
FROM Vehicle AS v
WHERE v.CurrentMileage > 100000;
