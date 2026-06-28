"""
=========================================================
FACT INVENTORY SNAPSHOT GENERATOR
=========================================================

Grain:
One row = One Product in One Warehouse
at one Snapshot Date
"""

import random
from pathlib import Path

import numpy as np
import pandas as pd

# =====================================================
# RANDOM SEED
# =====================================================

random.seed(42)
np.random.seed(42)

# =====================================================
# PATHS
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

GENERATED_FOLDER = PROJECT_ROOT / "data" / "generated"

OUTPUT_FILE = GENERATED_FOLDER / "fact_inventory_snapshot.csv"

# =====================================================
# LOAD DIMENSIONS
# =====================================================

dim_date = pd.read_csv(
    GENERATED_FOLDER / "dim_date.csv"
)

dim_product = pd.read_csv(
    GENERATED_FOLDER / "dim_product.csv"
)

dim_warehouse = pd.read_csv(
    GENERATED_FOLDER / "dim_warehouse.csv"
)
print(dim_warehouse["IsActive"].unique())
# =====================================================
# SNAPSHOT DATE
# =====================================================

# Latest date available in dim_date

SNAPSHOT_DATE_KEY = int(
    dim_date["DateKey"].max()
)

# =====================================================
# WAREHOUSE TYPE → PRODUCT CATEGORY MAPPING
# =====================================================

WAREHOUSE_CATEGORY_MAP = {

    "Regional Warehouse": [

        "Electronics",
        "Fashion",
        "Home & Kitchen",
        "Beauty",
        "Books",
        "Sports",
        "Grocery"

    ],

    "Fulfillment Center": [

        "Electronics",
        "Fashion",
        "Home & Kitchen",
        "Beauty"

    ],

    "Sort Center": [

        "Electronics",
        "Fashion"

    ]

}

# =====================================================
# INVENTORY ID
# =====================================================

def generate_inventory_id(number):

    return f"INV{number:08d}"


# =====================================================
# PRODUCT SELECTION
# =====================================================

def get_products_for_warehouse(warehouse):

    warehouse_type = warehouse["WarehouseType"]

    allowed_categories = WAREHOUSE_CATEGORY_MAP.get(
        warehouse_type,
        []
    )

    return dim_product[
        dim_product["Category"].isin(
            allowed_categories
        )
    ]


# =====================================================
# OPENING STOCK
# =====================================================

def generate_opening_stock(capacity):

    if capacity >= 50000:

        return random.randint(800, 1500)

    elif capacity >= 30000:

        return random.randint(400, 900)

    return random.randint(150, 450)


# =====================================================
# RECEIVED STOCK
# =====================================================

def generate_received_stock(opening_stock):

    return random.randint(

        0,

        int(opening_stock * 0.30)

    )


# =====================================================
# SOLD STOCK
# =====================================================

def generate_sold_stock(

    opening_stock,

    received_stock

):

    available_stock = opening_stock + received_stock

    minimum = int(available_stock * 0.20)

    maximum = int(available_stock * 0.80)

    return random.randint(

        minimum,

        maximum

    )


# =====================================================
# DAMAGED STOCK
# =====================================================

def generate_damaged_stock():

    return random.randint(

        0,

        10

    )


# =====================================================
# CLOSING STOCK
# =====================================================

def calculate_closing_stock(

    opening_stock,

    received_stock,

    sold_stock,

    damaged_stock

):

    return (

        opening_stock

        + received_stock

        - sold_stock

        - damaged_stock

    )


# =====================================================
# REORDER LEVEL
# =====================================================

def generate_reorder_level(capacity):

    if capacity >= 50000:

        return 250

    elif capacity >= 30000:

        return 150

    return 75


# =====================================================
# STOCK STATUS
# =====================================================

def determine_stock_status(

    closing_stock,

    reorder_level

):

    if closing_stock <= reorder_level:

        return "Low Stock"

    elif closing_stock <= reorder_level * 2:

        return "Medium Stock"

    return "Healthy"


# =====================================================
# FACT INVENTORY SNAPSHOT GENERATOR
# =====================================================

def generate_fact_inventory_snapshot():

    rows = []

    inventory_number = 1

    # ---------------------------------------------
    # Active Warehouses Only
    # ---------------------------------------------

    active_warehouses = dim_warehouse[
        dim_warehouse["IsActive"] == True
    ]

    # ---------------------------------------------
    # Loop through Warehouses
    # ---------------------------------------------

    for _, warehouse in active_warehouses.iterrows():

        warehouse_id = warehouse["WarehouseID"]

        capacity = warehouse["Capacity"]

        # Products applicable for this warehouse
        products = get_products_for_warehouse(warehouse)

        # ---------------------------------------------
        # Loop through Products
        # ---------------------------------------------

        for _, product in products.iterrows():

            opening_stock = generate_opening_stock(
                capacity
            )

            received_stock = generate_received_stock(
                opening_stock
            )

            sold_stock = generate_sold_stock(
                opening_stock,
                received_stock
            )

            damaged_stock = generate_damaged_stock()

            closing_stock = calculate_closing_stock(
                opening_stock,
                received_stock,
                sold_stock,
                damaged_stock
            )

            # Safety check
            if closing_stock < 0:
                closing_stock = 0

            reorder_level = generate_reorder_level(
                capacity
            )

            stock_status = determine_stock_status(
                closing_stock,
                reorder_level
            )

            rows.append({

                "InventoryID":
                    generate_inventory_id(
                        inventory_number
                    ),

                "SnapshotDateKey":
                    SNAPSHOT_DATE_KEY,

                "WarehouseID":
                    warehouse_id,

                "ProductID":
                    product["ProductID"],

                "OpeningStock":
                    opening_stock,

                "ReceivedStock":
                    received_stock,

                "SoldStock":
                    sold_stock,

                "DamagedStock":
                    damaged_stock,

                "ClosingStock":
                    closing_stock,

                "ReorderLevel":
                    reorder_level,

                "StockStatus":
                    stock_status

            })

            inventory_number += 1

    return pd.DataFrame(rows)


# =====================================================
# VALIDATION
# =====================================================

def validate_data(inventory_df):

    print("\nRunning validations...")

    # ---------------------------------------------
    # Duplicate InventoryID
    # ---------------------------------------------

    duplicate_count = inventory_df["InventoryID"].duplicated().sum()

    if duplicate_count > 0:

        raise ValueError(
            f"Duplicate InventoryID found : {duplicate_count}"
        )

    # ---------------------------------------------
    # Null Checks
    # ---------------------------------------------

    required_columns = [

        "InventoryID",

        "SnapshotDateKey",

        "WarehouseID",

        "ProductID",

        "OpeningStock",

        "ClosingStock"

    ]

    for column in required_columns:

        if inventory_df[column].isnull().any():

            raise ValueError(

                f"Null values found in {column}"

            )

    # ---------------------------------------------
    # Stock Validation
    # ---------------------------------------------

    if (inventory_df["OpeningStock"] < 0).any():

        raise ValueError(

            "Negative OpeningStock found."

        )

    if (inventory_df["ReceivedStock"] < 0).any():

        raise ValueError(

            "Negative ReceivedStock found."

        )

    if (inventory_df["SoldStock"] < 0).any():

        raise ValueError(

            "Negative SoldStock found."

        )

    if (inventory_df["DamagedStock"] < 0).any():

        raise ValueError(

            "Negative DamagedStock found."

        )

    if (inventory_df["ClosingStock"] < 0).any():

        raise ValueError(

            "Negative ClosingStock found."

        )

    # ---------------------------------------------
    # Closing Stock Formula Validation
    # ---------------------------------------------

    calculated = (

        inventory_df["OpeningStock"]

        + inventory_df["ReceivedStock"]

        - inventory_df["SoldStock"]

        - inventory_df["DamagedStock"]

    )

    mismatch = (

        calculated != inventory_df["ClosingStock"]

    ).sum()

    if mismatch > 0:

        raise ValueError(

            f"ClosingStock mismatch found : {mismatch}"

        )

    print("✅ All validations passed.")



# =====================================================
# EXPORT
# =====================================================

def export_csv(inventory_df):

    GENERATED_FOLDER.mkdir(

        parents=True,

        exist_ok=True

    )

    inventory_df.to_csv(

        OUTPUT_FILE,

        index=False

    )

    print(

        f"\nInventory Snapshot saved to:\n{OUTPUT_FILE}"

    )


# =====================================================
# MAIN
# =====================================================

def main():

    print("\nGenerating Inventory Snapshot...\n")

    inventory_df = generate_fact_inventory_snapshot()

    validate_data(

        inventory_df

    )

    export_csv(

        inventory_df

    )

    print(

        "\nInventory Snapshot Generated Successfully."

    )


if __name__ == "__main__":

    main()

