-- ex2.sql
-- Create Database
CREATE DATABASE SMILES;
USE SMILES;

-- Staff table
CREATE TABLE Staff(
  StaffNo INT AUTO_INCREMENT PRIMARY KEY,
  fName VARCHAR(50) NOT NULL,
  lName VARCHAR(50) NOT NULL,
  Address VARCHAR(255),
  PhoneNo VARCHAR(20),
  DOB DATE NOT NULL,
  Sex CHAR(1) CHECK (Sex IN ('F','M')),
  NIN VARCHAR(20) NOT NULL UNIQUE,
  DateJoined DATE,
  JobTitle VARCHAR(20),
  Salary DECIMAL(10,2)
);

-- Outlet table
CREATE TABLE Outlet(
  OutletNo INT AUTO_INCREMENT PRIMARY KEY,
  Address VARCHAR(255),
  PhoneNo VARCHAR(20),
  FaxNo VARCHAR(20),
  Manager INT,
  FOREIGN KEY (Manager) REFERENCES Staff(StaffNo) ON DELETE SET NULL
);

-- Vehicle table
CREATE TABLE Vehicle(
    RegistrationNo VARCHAR(20) PRIMARY KEY,
    PlateNo VARCHAR(20) NOT NULL UNIQUE,
    Type VARCHAR(50),
    FuelType VARCHAR(20),
    Model VARCHAR(20),
    Make VARCHAR(30),
    EngineSize VARCHAR(20),
    Capacity INT,
    CurrentMileage INT,
    MOTDue DATE,
    HireRate DECIMAL(10,2) NOT NULL,
    CurrentLocation INT,
    FOREIGN KEY (CurrentLocation) REFERENCES Outlet(OutletNo) ON DELETE SET NULL,
    Status ENUM('Available', 'Hired', 'Under Maintenance', 'Out of Service') DEFAULT 'Available',
    InsuranceExpiry DATE
);

-- Parent Table: Client 
CREATE TABLE Client (
    ClientNo INT AUTO_INCREMENT PRIMARY KEY,
    fName VARCHAR(50),
    lName VARCHAR(50),
    Address VARCHAR(255),
    Telephone VARCHAR(20),
    Email VARCHAR(100),
    LoyaltyPoints INT
);

-- Subclass: PersonalClient
CREATE TABLE PersonalClient (
    ClientNo INT PRIMARY KEY,
    DOB DATE NOT NULL,
    LicenceNo VARCHAR(20) NOT NULL UNIQUE,
    FOREIGN KEY (ClientNo) REFERENCES Client(ClientNo) ON DELETE CASCADE
);

-- Subclass: BusinessClient
CREATE TABLE BusinessClient (
    ClientNo INT PRIMARY KEY,
    BusinessName VARCHAR(100) NOT NULL,
    BusinessType VARCHAR(50),
    FaxNo VARCHAR(20),
    FOREIGN KEY (ClientNo) REFERENCES Client(ClientNo) ON DELETE CASCADE
);

-- HireAgreement table
CREATE TABLE HireAgreement (
    HireNo INT AUTO_INCREMENT PRIMARY KEY,  
    ClientNo INT NOT NULL,
    VehicleRegNo VARCHAR(20) NOT NULL,
    StartDate DATE NOT NULL,  
    TerminationDate DATE NOT NULL, 
    RentalDuration INT GENERATED ALWAYS AS (DATEDIFF(TerminationDate, StartDate)) STORED,  
    PreHireMileage INT NOT NULL,  
    PostHireMileage INT NOT NULL,  
    CurrentMileage INT GENERATED ALWAYS AS (PostHireMileage - PreHireMileage) STORED,  
    TotalCost DECIMAL(10,2) NOT NULL,  
    PaymentMethod ENUM('Cash', 'Credit Card', 'Debit Card', 'Online Transfer') NOT NULL, 
    PaymentStatus ENUM('Pending', 'Paid', 'Failed', 'Refunded') DEFAULT 'Pending',
    DepositAmount DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (ClientNo) REFERENCES Client(ClientNo) ON DELETE CASCADE,
    FOREIGN KEY (VehicleRegNo) REFERENCES Vehicle(RegistrationNo) ON DELETE CASCADE
);

-- FaultReport table
CREATE TABLE FaultReport (
    FaultID INT AUTO_INCREMENT PRIMARY KEY,  
    VehicleRegNo VARCHAR(20) NOT NULL,
    StaffNo INT NOT NULL,
    ReportDate DATE NOT NULL, 
    FaultDescription TEXT NOT NULL,  
    DateChecked DATE, 
    FaultFound ENUM('Y', 'N') NOT NULL DEFAULT 'N',
    FOREIGN KEY (VehicleRegNo) REFERENCES Vehicle(RegistrationNo) ON DELETE CASCADE,
    FOREIGN KEY (StaffNo) REFERENCES Staff(StaffNo) ON DELETE CASCADE
);

-- Describe relations
DESCRIBE Staff;
DESCRIBE Outlet;
DESCRIBE Vehicle;
DESCRIBE Client;
DESCRIBE PersonalClient;
DESCRIBE BusinessClient;
DESCRIBE HireAgreement;
DESCRIBE FaultReport;
