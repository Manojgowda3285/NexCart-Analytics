"""
==========================================================
DIM WAREHOUSE GENERATOR
==========================================================

Generates Warehouse Dimension
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

TOTAL_WAREHOUSES = 30

WAREHOUSE_TYPES = [

    "Fulfillment Center",

    "Regional Warehouse",

    "Sort Center"

]

# ------------------------------------------------------
# ID HELPERS
# ------------------------------------------------------

def generate_warehouse_id(number):

    return f"W{number:06d}"


def generate_warehouse_code(number):

    return f"WH{number:06d}"


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
# RANDOM DATE
# ------------------------------------------------------

def random_opening_date():

    start = datetime(2018,1,1)

    end = datetime.today()

    days = (end-start).days

    return start + timedelta(

        days=random.randint(0,days)

    )


# ------------------------------------------------------
# CAPACITY
# ------------------------------------------------------

def generate_capacity():

    bucket = random.choices(

        ["Small","Medium","Large","Mega"],

        weights=[20,35,30,15]

    )[0]

    if bucket == "Small":

        return random.randint(50000,90000)

    elif bucket == "Medium":

        return random.randint(120000,180000)

    elif bucket == "Large":

        return random.randint(250000,350000)

    else:

        return random.randint(450000,550000)


# ------------------------------------------------------
# OPERATING COST
# ------------------------------------------------------

def generate_operating_cost(capacity):

    if capacity < 100000:

        return random.randint(400000,600000)

    elif capacity < 200000:

        return random.randint(700000,1000000)

    elif capacity < 400000:

        return random.randint(1200000,1800000)

    else:

        return random.randint(2000000,2800000)
    
# ------------------------------------------------------
# WAREHOUSE GENERATOR
# ------------------------------------------------------

def generate_warehouse_dimension():

    locations = load_locations()

    rows = []

    for warehouse_number in range(1, TOTAL_WAREHOUSES + 1):

        # --------------------------------------------
        # Warehouse Type
        # --------------------------------------------

        warehouse_type = random.choices(

            WAREHOUSE_TYPES,

            weights=[60, 30, 10]

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
        # Warehouse Name
        # --------------------------------------------

        warehouse_name = (f"{city} "f"{warehouse_type} "f"{warehouse_number:02d}")

        # --------------------------------------------
        # Capacity
        # --------------------------------------------

        capacity = generate_capacity()

        # --------------------------------------------
        # Operating Cost
        # --------------------------------------------

        operating_cost = generate_operating_cost(capacity)

        # --------------------------------------------
        # Manager
        # --------------------------------------------

        manager_name = fake.name()

        # --------------------------------------------
        # Contact Number
        # --------------------------------------------

        contact_number = fake.msisdn()[-10:]

        # --------------------------------------------
        # Temperature Controlled
        # --------------------------------------------

        temperature_controlled = random.choices(

            [True, False],

            weights=[25, 75]

        )[0]

        # --------------------------------------------
        # Active
        # --------------------------------------------

        is_active = random.choices(

            [True, False],

            weights=[95, 5]

        )[0]

        # --------------------------------------------
        # Opening Date
        # --------------------------------------------

        opening_date = random_opening_date()

        # --------------------------------------------
        # Create Row
        # --------------------------------------------

        rows.append({

            "WarehouseID":
                generate_warehouse_id(warehouse_number),

            "WarehouseCode":
                generate_warehouse_code(warehouse_number),

            "WarehouseName":
                warehouse_name,

            "WarehouseType":
                warehouse_type,

            "City":
                city,

            "State":
                state,

            "Region":
                region,

            "Pincode":
                pincode,

            "Capacity":
                capacity,

            "ManagerName":
                manager_name,

            "ContactNumber":
                contact_number,

            "TemperatureControlled":
                temperature_controlled,

            "OperatingCostPerMonth":
                operating_cost,

            "OpeningDate":
                opening_date.date(),

            "IsActive":
                is_active

        })

    warehouses = pd.DataFrame(rows)

    return warehouses

# ------------------------------------------------------
# VALIDATION
# ------------------------------------------------------

def validate_warehouse_dimension(warehouses):

    print("\nRunning Warehouse Dimension Validation...")

    # ---------------------------------------------
    # Duplicate WarehouseID
    # ---------------------------------------------

    duplicate_id = warehouses["WarehouseID"].duplicated().sum()

    if duplicate_id > 0:
        raise ValueError(
            f"Duplicate WarehouseID found. Count={duplicate_id}"
        )

    # ---------------------------------------------
    # Duplicate WarehouseCode
    # ---------------------------------------------

    duplicate_code = warehouses["WarehouseCode"].duplicated().sum()

    if duplicate_code > 0:
        raise ValueError(
            f"Duplicate WarehouseCode found. Count={duplicate_code}"
        )

    # ---------------------------------------------
    # Null Values
    # ---------------------------------------------

    null_count = warehouses.isnull().sum().sum()

    if null_count > 0:

        print(warehouses.isnull().sum())

        raise ValueError(
            f"Null values found. Count={null_count}"
        )

    # ---------------------------------------------
    # Capacity Validation
    # ---------------------------------------------

    if (warehouses["Capacity"] <= 0).any():
        raise ValueError(
            "Capacity should always be greater than zero."
        )

    # ---------------------------------------------
    # Operating Cost Validation
    # ---------------------------------------------

    if (warehouses["OperatingCostPerMonth"] <= 0).any():
        raise ValueError(
            "Operating Cost should always be greater than zero."
        )

    # ---------------------------------------------
    # Contact Number Validation
    # ---------------------------------------------

    invalid_contact = (
        warehouses["ContactNumber"]
        .astype(str)
        .str.len() != 10
    )

    if invalid_contact.any():
        raise ValueError(
            "Invalid Contact Number detected."
        )

    print("✓ Warehouse Dimension Validation Passed")


# ------------------------------------------------------
# EXPORT
# ------------------------------------------------------

def export_warehouse_dimension(warehouses):

    output_file = OUTPUT_FOLDER / "dim_warehouse.csv"

    warehouses.to_csv(
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
    print("Generating Warehouse Dimension")
    print("=" * 60)

    warehouses = generate_warehouse_dimension()

    print(
        f"\nGenerated {len(warehouses)} warehouses."
    )

    validate_warehouse_dimension(warehouses)

    export_warehouse_dimension(warehouses)

    print("\nWarehouse Dimension Completed Successfully.")

         


if __name__ == "__main__":

    main()

    