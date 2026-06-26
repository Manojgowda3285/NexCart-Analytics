"""
==========================================================
DIM SELLER GENERATOR
==========================================================

Generates Seller Dimension
for Indian E-Commerce Analytics Platform.

Author : Manoj M
"""

import json
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

TOTAL_SELLERS = 500

SELLER_TYPES = [
    "Business",
    "Individual"
]

BUSINESS_CATEGORIES = [
    "Electronics",
    "Fashion",
    "Home & Kitchen",
    "Beauty",
    "Grocery",
    "Books",
    "Sports"
]

FULFILLMENT_TYPES = [
    "Warehouse Fulfilled",
    "Seller Fulfilled"
]

COMMISSION_RULES = {

    "Electronics": (10,15),

    "Fashion": (18,25),

    "Home & Kitchen": (10,16),

    "Beauty": (12,18),

    "Grocery": (4,8),

    "Books": (8,12),

    "Sports": (10,15)

}


# ------------------------------------------------------
# ID HELPERS
# ------------------------------------------------------

def generate_seller_id(number):

    return f"S{number:06d}"


def generate_seller_code(number):

    return f"SELL{number:06d}"


# ------------------------------------------------------
# CONFIG LOADER
# ------------------------------------------------------

def load_locations():

    with open(
        CONFIG_FOLDER / "indian_locations.json",
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# ------------------------------------------------------
# DATE
# ------------------------------------------------------

def random_registration_date():

    start = datetime(2022,1,1)

    end = datetime.today()

    days = (end-start).days

    return start + timedelta(

        days=random.randint(0,days)

    )

# ------------------------------------------------------
# SELLER GENERATOR
# ------------------------------------------------------

def generate_seller_dimension():

    locations = load_locations()

    rows = []

    for seller_number in range(1, TOTAL_SELLERS + 1):

        # --------------------------------------------
        # Category
        # --------------------------------------------

        category = random.choice(BUSINESS_CATEGORIES)

        # --------------------------------------------
        # Seller Name
        # --------------------------------------------

        company_prefix = random.choice([

            "Tech",
            "Shree",
            "Sai",
            "Global",
            "Prime",
            "Royal",
            "Smart",
            "Elite",
            "Modern",
            "National"

        ])

        company_suffix = random.choice([

            "Traders",
            "Enterprises",
            "Retail",
            "Mart",
            "Store",
            "Solutions",
            "Distributors",
            "Suppliers",
            "Hub",
            "World"

        ])

        seller_name = ( f"{company_prefix} "f"{category} "f"{company_suffix} "f"{seller_number:03d}")

        # --------------------------------------------
        # Seller Type
        # --------------------------------------------

        seller_type = random.choices(

            SELLER_TYPES,

            weights=[80,20]

        )[0]

        # --------------------------------------------
        # Location (Weighted)
        # --------------------------------------------

        location = random.choices(

            locations,

            weights=[

                loc["Weight"]

                for loc in locations

            ],

            k=1

        )[0]

        city = location["City"]

        state = location["State"]

        region = location["Region"]

        pincode = location["Pincode"]

        # --------------------------------------------
        # Registration
        # --------------------------------------------

        registration_date = random_registration_date()

        # --------------------------------------------
        # Rating
        # --------------------------------------------

        seller_rating = round(

            random.triangular(

                3.5,

                5.0,

                4.6

            ),

            1

        )

        # --------------------------------------------
        # Commission
        # --------------------------------------------

        minimum, maximum = COMMISSION_RULES[category]

        commission_rate = round(

            random.uniform(

                minimum,

                maximum

            ),

            2

        )

        # --------------------------------------------
        # Verification
        # --------------------------------------------

        is_verified = random.choices(

            [True, False],

            weights=[90,10]

        )[0]

        # --------------------------------------------
        # Active
        # --------------------------------------------

        is_active = random.choices(

            [True, False],

            weights=[95,5]

        )[0]

        # --------------------------------------------
        # Fulfillment
        # --------------------------------------------

        fulfillment_type = random.choices(

            FULFILLMENT_TYPES,

            weights=[70,30]

        )[0]

        # --------------------------------------------
        # GST
        # --------------------------------------------

        gst_number = fake.gstin()

        # --------------------------------------------
        # PAN
        # --------------------------------------------

        pan_number = fake.bothify(

            text="?????####?"

        ).upper()

        # --------------------------------------------
        # Create Record
        # --------------------------------------------

        rows.append({

            "SellerID":
                generate_seller_id(seller_number),

            "SellerCode":
                generate_seller_code(seller_number),

            "SellerName":
                seller_name,

            "SellerType":
                seller_type,

            "BusinessCategory":
                category,

            "GSTNumber":
                gst_number,

            "PANNumber":
                pan_number,

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

            "SellerRating":
                seller_rating,

            "CommissionRate":
                commission_rate,

            "FulfillmentType":
                fulfillment_type,

            "IsVerified":
                is_verified,

            "IsActive":
                is_active

        })

    sellers = pd.DataFrame(rows)

    return sellers

# ------------------------------------------------------
# VALIDATION
# ------------------------------------------------------

def validate_seller_dimension(sellers):

    print("\nRunning Seller Dimension Validation...")

    # ---------------------------------------------
    # Duplicate SellerID
    # ---------------------------------------------

    duplicate_seller_id = sellers["SellerID"].duplicated().sum()

    if duplicate_seller_id > 0:
        raise ValueError(
            f"Duplicate SellerID found. Count={duplicate_seller_id}"
        )

    # ---------------------------------------------
    # Duplicate SellerCode
    # ---------------------------------------------

    duplicate_seller_code = sellers["SellerCode"].duplicated().sum()

    if duplicate_seller_code > 0:
        raise ValueError(
            f"Duplicate SellerCode found. Count={duplicate_seller_code}"
        )

    # ---------------------------------------------
    # Null Values
    # ---------------------------------------------

    null_count = sellers.isnull().sum().sum()

    if null_count > 0:

        print(sellers.isnull().sum())

        raise ValueError(
            f"Null values found. Count={null_count}"
        )

    # ---------------------------------------------
    # Rating Validation
    # ---------------------------------------------

    if not sellers["SellerRating"].between(3.5, 5.0).all():
        raise ValueError(
            "Seller Rating must be between 3.5 and 5.0"
        )

    # ---------------------------------------------
    # Commission Validation
    # ---------------------------------------------

    if (sellers["CommissionRate"] <= 0).any():
        raise ValueError(
            "Commission Rate cannot be negative."
        )

    # ---------------------------------------------
    # GST Validation
    # ---------------------------------------------

    invalid_gst = sellers["GSTNumber"].astype(str).str.len() != 15

    if invalid_gst.any():
        raise ValueError(
            "Invalid GST Number detected."
        )

    # ---------------------------------------------
    # PAN Validation
    # ---------------------------------------------

    invalid_pan = sellers["PANNumber"].astype(str).str.len() != 10

    if invalid_pan.any():
        raise ValueError(
            "Invalid PAN Number detected."
        )

    print("✓ Seller Dimension Validation Passed")


# ------------------------------------------------------
# EXPORT
# ------------------------------------------------------

def export_seller_dimension(sellers):

    output_file = OUTPUT_FOLDER / "dim_seller.csv"

    sellers.to_csv(
        output_file,
        index=False
    )

    print("\nCSV exported successfully.")

    print(output_file)


# ------------------------------------------------------
# MAIN
# ------------------------------------------------------

def main():

    print("=" * 60)
    print("Generating Seller Dimension")
    print("=" * 60)

    sellers = generate_seller_dimension()

    print(f"\nGenerated {len(sellers)} sellers.")

    validate_seller_dimension(sellers)

    export_seller_dimension(sellers)

    print("\nSeller Dimension Completed Successfully.")


if __name__ == "__main__":

    main()