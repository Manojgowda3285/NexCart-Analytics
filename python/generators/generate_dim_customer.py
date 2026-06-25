"""
==========================================================
DIM CUSTOMER GENERATOR
==========================================================

Generates Customer Dimension
for Indian E-Commerce Analytics Platform.

Author : Manoj M
"""

import random
from pathlib import Path
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from faker import Faker

fake = Faker("en_IN")

random.seed(42)
np.random.seed(42)
Faker.seed(42)


# ------------------------------------------------------
# PATHS
# ------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

CONFIG_FOLDER = PROJECT_ROOT / "config"

OUTPUT_FOLDER = PROJECT_ROOT / "data" / "generated"

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------
# CONFIG
# ------------------------------------------------------

TOTAL_CUSTOMERS = 5000


# ------------------------------------------------------
# STATIC DATA
# ------------------------------------------------------

AGE_GROUPS = [

    (18,24,"18-24"),
    (25,34,"25-34"),
    (35,44,"35-44"),
    (45,54,"45-54"),
    (55,65,"55+")

]

CUSTOMER_SEGMENTS = [

    "New",

    "Regular",

    "Premium"

]

PREFERRED_CATEGORIES = [

    "Electronics",

    "Fashion",

    "Home & Kitchen",

    "Grocery",

    "Beauty",

    "Sports",

    "Books"

]


# ------------------------------------------------------
# ID GENERATORS
# ------------------------------------------------------

def generate_customer_id(number):

    return f"C{number:06d}"


def generate_customer_code(number):

    return f"CUST{number:06d}"


# ------------------------------------------------------
# AGE
# ------------------------------------------------------

def calculate_age(dob):

    today = datetime.today().date()

    return today.year - dob.year - (

        (today.month, today.day)

        <

        (dob.month, dob.day)

    )


def get_age_group(age):

    for start, end, label in AGE_GROUPS:

        if start <= age <= end:

            return label

    return "55+"


# ------------------------------------------------------
# RANDOM HELPERS
# ------------------------------------------------------

def random_registration_date():

    start = datetime(2023,1,1)

    end = datetime.today()

    days = (end-start).days

    return start + timedelta(

        days=random.randint(0,days)

    )

import json


# ------------------------------------------------------
# LOAD LOCATIONS
# ------------------------------------------------------

def load_locations():

    file_path = CONFIG_FOLDER / "indian_locations.json"

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


# ------------------------------------------------------
# CUSTOMER GENERATOR
# ------------------------------------------------------

def generate_customer_dimension():

    locations = load_locations()

    rows = []

    for customer_number in range(1, TOTAL_CUSTOMERS + 1):

        # ------------------------------
        # Name
        # ------------------------------

        gender = random.choice(["Male", "Female"])

        if gender == "Male":
            first_name = fake.first_name_male()
        else:
            first_name = fake.first_name_female()

        last_name = fake.last_name()

        full_name = f"{first_name} {last_name}"

        # ------------------------------
        # Date of Birth
        # ------------------------------

        dob = fake.date_of_birth(
            minimum_age=18,
            maximum_age=60
        )

        age = calculate_age(dob)

        age_group = get_age_group(age)

        # ------------------------------
        # Location
        # ------------------------------

        location = random.choice(locations)

        city = location["City"]

        state = location["State"]

        region = location["Region"]

        pincode = location["Pincode"]

        # ------------------------------
        # Registration
        # ------------------------------

        registration_date = random_registration_date()

        # ------------------------------
        # Customer Segment
        # ------------------------------

        customer_segment = random.choices(

            CUSTOMER_SEGMENTS,

            weights=[30, 55, 15]

        )[0]

        # ------------------------------
        # Preferred Category
        # ------------------------------

        preferred_category = random.choice(
            PREFERRED_CATEGORIES
        )

        # ------------------------------
        # Prime Member
        # ------------------------------

        is_prime = random.choices(

            [True, False],

            weights=[35, 65]

        )[0]

        # ------------------------------
        # Active Customer
        # ------------------------------

        is_active = random.choices(

            [True, False],

            weights=[92, 8]

        )[0]

        # ------------------------------
        # Email
        # ------------------------------

        email = (
            first_name.lower()
            + "."
            + last_name.lower()
            + str(random.randint(10,999))
            + "@gmail.com"
        )

        # ------------------------------
        # Phone
        # ------------------------------

        phone = fake.msisdn()[-10:]

        # ------------------------------
        # Create Row
        # ------------------------------

        rows.append({

            "CustomerID":
                generate_customer_id(customer_number),

            "CustomerCode":
                generate_customer_code(customer_number),

            "FirstName":
                first_name,

            "LastName":
                last_name,

            "FullName":
                full_name,

            "Gender":
                gender,

            "DOB":
                dob,

            "Age":
                age,

            "AgeGroup":
                age_group,

            "Email":
                email,

            "Phone":
                phone,

            "City":
                city,

            "State":
                state,

            "Region":
                region,

            "Pincode":
                pincode,

            "RegistrationDate":
                registration_date.date(),

            "CustomerSegment":
                customer_segment,

            "PreferredCategory":
                preferred_category,

            "IsPrimeMember":
                is_prime,

            "IsActive":
                is_active

        })

    customers = pd.DataFrame(rows)

    return customers

# ------------------------------------------------------
# VALIDATION
# ------------------------------------------------------

def validate_customer_dimension(customers):

    print("\nRunning Customer Dimension Validation...")

    # ---------------------------------------------
    # Duplicate CustomerID
    # ---------------------------------------------

    duplicate_customer_id = customers["CustomerID"].duplicated().sum()

    if duplicate_customer_id > 0:
        raise ValueError(
            f"Duplicate CustomerID found. Count={duplicate_customer_id}"
        )

    # ---------------------------------------------
    # Duplicate CustomerCode
    # ---------------------------------------------

    duplicate_customer_code = customers["CustomerCode"].duplicated().sum()

    if duplicate_customer_code > 0:
        raise ValueError(
            f"Duplicate CustomerCode found. Count={duplicate_customer_code}"
        )

    # ---------------------------------------------
    # Null Check
    # ---------------------------------------------

    null_count = customers.isnull().sum().sum()

    if null_count > 0:
        print(customers.isnull().sum())
        raise ValueError(
            f"Null values found. Count={null_count}"
        )

    # ---------------------------------------------
    # Age Validation
    # ---------------------------------------------

    if not customers["Age"].between(18, 60).all():
        raise ValueError(
            "Age must be between 18 and 60."
        )

    # ---------------------------------------------
    # Email Validation
    # ---------------------------------------------

    if (~customers["Email"].str.contains("@")).any():
        raise ValueError(
            "Invalid email addresses found."
        )

    # ---------------------------------------------
    # Phone Validation
    # ---------------------------------------------

    invalid_phone = customers["Phone"].astype(str).str.len() != 10

    if invalid_phone.any():
        raise ValueError(
            "Invalid phone numbers found."
        )

    print("✓ Customer Dimension Validation Passed")


# ------------------------------------------------------
# EXPORT
# ------------------------------------------------------

def export_customer_dimension(customers):

    output_file = OUTPUT_FOLDER / "dim_customer.csv"

    customers.to_csv(
        output_file,
        index=False
    )

    print(f"\nCSV exported successfully.")

    print(output_file)


# ------------------------------------------------------
# MAIN
# ------------------------------------------------------

def main():

    print("=" * 60)
    print("Generating Customer Dimension")
    print("=" * 60)

    customers = generate_customer_dimension()

    print(
        f"\nGenerated {len(customers)} customers."
    )

    validate_customer_dimension(customers)

    export_customer_dimension(customers)

    print("\nCustomer Dimension Completed Successfully.")


if __name__ == "__main__":

    main()