import mysql.connector
from faker import Faker
import random

# Initialize Faker
fake = Faker()

# Connect to MySQL Database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="0426Mandy+", 
    database="SMILES"
)
cursor = conn.cursor()

# Function to Insert Clients
def insert_clients(n=100):
    try:
        cursor.execute("SELECT COUNT(*) FROM Client")
        existing_clients = cursor.fetchone()[0]
        
        if existing_clients >= n:
            print("Clients already exist, skipping insertion.")
            return

        for _ in range(existing_clients, n):
            fName = fake.first_name()
            lName = fake.last_name()
            address = fake.address().replace("\n", ", ")
            phone = fake.phone_number()[:10]
            email = fake.email()
            loyalty = random.randint(0, 500)

            cursor.execute("""
                INSERT INTO Client (fName, lName, Address, Telephone, Email, LoyaltyPoints)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (fName, lName, address, phone, email, loyalty))

        conn.commit()
        print(f"✅ {n} Clients Inserted Successfully!")
    except mysql.connector.Error as e:
        print(f"❌ Error inserting Clients: {e}")

# ✅ Function to Insert Outlets
def insert_outlets(n=30):
    try:
        cursor.execute("SELECT COUNT(*) FROM Outlet")
        existing_outlets = cursor.fetchone()[0]
        
        if existing_outlets >= n:
            print("✅ Outlets already exist, skipping insertion.")
            return

        for i in range(existing_outlets + 1, existing_outlets + n + 1):  
            address = fake.address().replace("\n", ", ")
            phone = fake.phone_number()[:10]
            fax = fake.phone_number()[:10]

            cursor.execute("""
                INSERT INTO Outlet (OutletNo, Address, PhoneNo, FaxNo)
                VALUES (%s, %s, %s, %s)
            """, (i, address, phone, fax))

        conn.commit()
        print(f"✅ {n} Outlets Inserted Successfully!")
    except mysql.connector.Error as e:
        print(f"❌ Error inserting Outlets: {e}")

# ✅ Function to Insert Vehicles
def insert_vehicles(n=50):
    try:
        cursor.execute("SELECT COUNT(*) FROM Vehicle")
        existing_vehicles = cursor.fetchone()[0]

        cursor.execute("SELECT OutletNo FROM Outlet")
        outlets = [row[0] for row in cursor.fetchall()]

        if not outlets:
            raise ValueError("No outlets available! Insert outlets first.")

        for i in range(existing_vehicles, existing_vehicles + n):
            reg_no = f"V{1000 + i}"  # Ensures unique registration numbers
            plate_no = f"SGX{random.randint(1000, 9999)}{random.choice(['A', 'B', 'C', 'D'])}"
            vehicle_type = random.choice(["Car", "Van", "SUV"])
            fuel_type = random.choice(["Petrol", "Diesel", "Electric"])
            model = fake.word()
            make = fake.company()
            engine_size = f"{random.uniform(1.0, 3.0):.1f}L"
            capacity = random.randint(2, 8)
            mileage = random.randint(5000, 150000)
            mot_due = fake.future_date()
            hire_rate = round(random.uniform(50, 200), 2)
            location = random.choice(outlets) 
            status = random.choice(["Available", "Hired", "Under Maintenance"])
            insurance_expiry = fake.future_date()

            cursor.execute("""
                INSERT INTO Vehicle (RegistrationNo, PlateNo, Type, FuelType, Model, Make, EngineSize, Capacity, CurrentMileage, MOTDue, HireRate, CurrentLocation, Status, InsuranceExpiry)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (reg_no, plate_no, vehicle_type, fuel_type, model, make, engine_size, capacity, mileage, mot_due, hire_rate, location, status, insurance_expiry))

        conn.commit()
        print(f"✅ {n} Vehicles Inserted Successfully!")
    except mysql.connector.Error as e:
        print(f"❌ Error inserting Vehicles: {e}")

# ✅ Function to Insert Hire Agreements
def insert_hire_agreements(n=50):
    try:
        cursor.execute("SELECT COUNT(*) FROM HireAgreement")
        existing_agreements = cursor.fetchone()[0]

        cursor.execute("SELECT ClientNo FROM Client")
        clients = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT RegistrationNo FROM Vehicle WHERE Status = 'Available'")
        vehicles = [row[0] for row in cursor.fetchall()]

        if not clients or not vehicles:
            raise ValueError("No Clients or Available Vehicles found! Insert data first.")

        for _ in range(existing_agreements, existing_agreements + n):
            client_no = random.choice(clients)  
            vehicle_reg_no = random.choice(vehicles)  

            start_date = fake.date_between(start_date="-60d", end_date="today")
            termination_date = fake.date_between(start_date=start_date, end_date="+30d")
            pre_hire_mileage = random.randint(5000, 100000)
            post_hire_mileage = pre_hire_mileage + random.randint(100, 500)
            total_cost = round(random.uniform(100, 600), 2)
            payment_method = random.choice(["Cash", "Credit Card", "Debit Card", "Online Transfer"])
            payment_status = random.choice(["Pending", "Paid", "Failed", "Refunded"])
            deposit_amount = round(random.uniform(50, 250), 2)

            cursor.execute("""
                INSERT INTO HireAgreement (ClientNo, VehicleRegNo, StartDate, TerminationDate, PreHireMileage, PostHireMileage, TotalCost, PaymentMethod, PaymentStatus, DepositAmount)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (client_no, vehicle_reg_no, start_date, termination_date, pre_hire_mileage, post_hire_mileage, total_cost, payment_method, payment_status, deposit_amount))

        conn.commit()
        print(f"✅ {n} Hire Agreements Inserted Successfully!")
    except mysql.connector.Error as e:
        print(f"❌ Error inserting Hire Agreements: {e}")

if __name__ == "__main__":
    insert_clients(100)  
    insert_outlets(30)  
    insert_vehicles(50) 
    insert_hire_agreements(50)  

    cursor.close()
    conn.close()
    print("✅ Data Insertion Completed!")