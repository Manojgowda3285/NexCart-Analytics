# import json
# import random
# from datetime import datetime, timedelta

# import numpy as np
# import pandas as pd



# VARIANTS = {

#     "Smartphones": [
#         "6GB/128GB/Blue",
#         "8GB/128GB/Black",
#         "8GB/256GB/Green"
#     ],

#     "Laptops": [
#         "8GB/512GB SSD",
#         "16GB/512GB SSD",
#         "16GB/1TB SSD"
#     ],

#     "Headphones": [
#         "Black",
#         "Blue",
#         "White"
#     ],

#     "Smart Watches": [
#         "Black Strap",
#         "Silver Strap"
#     ],

#     "Shoes": [
#         "Size 7",
#         "Size 8",
#         "Size 9",
#         "Size 10"
#     ],

#     "Men Clothing": [
#         "S",
#         "M",
#         "L",
#         "XL"
#     ],

#     "Women Clothing": [
#         "S",
#         "M",
#         "L",
#         "XL"
#     ],

#     "Staples": [
#         "1kg",
#         "5kg",
#         "10kg"
#     ],

#     "Snacks": [
#         "100g",
#         "250g",
#         "500g"
#     ],

#     "Beverages": [
#         "500ml",
#         "1L",
#         "2L"
#     ],

#     "Cookware": [
#         "2L",
#         "3L",
#         "5L"
#     ],

#     "Kitchen Appliances": [
#         "Standard"
#     ],

#     "Storage": [
#         "500ml",
#         "1L"
#     ],

#     "Skin Care": [
#         "100ml",
#         "200ml"
#     ],

#     "Hair Care": [
#         "180ml",
#         "340ml"
#     ],

#     "Refrigerator": [
#         "260L",
#         "320L",
#         "420L"
#     ],

#     "Washing Machine": [
#         "6kg",
#         "8kg",
#         "10kg"
#     ],

#     "Air Conditioner": [
#         "1 Ton",
#         "1.5 Ton",
#         "2 Ton"
#     ],

#     "Office": [
#         "Standard"
#     ],

#     "Bedroom": [
#         "Queen",
#         "King"
#     ],

#     "Fitness": [
#         "5kg",
#         "10kg",
#         "20kg"
#     ],

#     "Outdoor": [
#         "Standard"
#     ],

#     "Programming": [
#         "Paperback",
#         "Hardcover"
#     ],

#     "Business": [
#         "Paperback",
#         "Hardcover"
#     ],

#     "Educational": [
#         "Standard"
#     ],

#     "Kids": [
#         "Standard"
#     ]
# }


# def load_catalog(path):

#     with open(path, "r", encoding="utf-8") as file:
#         catalog = json.load(file)

#     return catalog



# def generate_products(catalog):

#     products = []

#     product_id = 1

#     for category, subcategories in catalog.items():

#         for subcategory, brands in subcategories.items():

#             variants = VARIANTS.get(subcategory, ["Standard"])

#             for brand, models in brands.items():

#                 for model in models:

#                     for variant in variants:

#                         products.append({

#                             "ProductID": f"P{product_id:06}",

#                             "Category": category,

#                             "SubCategory": subcategory,

#                             "Brand": brand,

#                             "Model": model,

#                             "Variant": variant

#                         })

#                         product_id += 1

#     return pd.DataFrame(products)

# def load_pricing_rules(path):

#     with open(path, "r", encoding="utf-8") as file:
#         rules = json.load(file)

#     return rules

# def add_product_attributes(products, pricing_rules):

#     cost_prices = []
#     margins = []
#     selling_prices = []
#     gst_list = []
#     weights = []
#     return_windows = []

#     for _, row in products.iterrows():

#         rule = pricing_rules[row["SubCategory"]]

#         # Business logic goes here
#         cost = random.randint(rule["cost_min"], rule["cost_max"])

#         margin = random.uniform(rule["margin_min"], rule["margin_max"])

#         selling_price = round(cost * (1 + margin/100))

#         gst = rule["gst"]

#         weight = random.uniform(rule["weight_min"], rule["weight_max"])


#     return products


"""
==========================================================
DIM_PRODUCT GENERATOR
==========================================================

Generates the Product Dimension for the E-Commerce Analytics
Platform.

Author : Manoj M
Project : Indian E-Commerce Analytics Platform

"""

import json
import random
from pathlib import Path

import numpy as np
import pandas as pd


# ----------------------------------------------------------
# Random Seed
# ----------------------------------------------------------

random.seed(42)
np.random.seed(42)


# ----------------------------------------------------------
# Project Paths
# ----------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

CONFIG_FOLDER = PROJECT_ROOT / "config"

OUTPUT_FOLDER = PROJECT_ROOT / "data" / "generated"

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)


# ----------------------------------------------------------
# Variant Master
# ----------------------------------------------------------

VARIANTS = {

    "Smartphones": [
        "6GB/128GB/Blue",
        "8GB/128GB/Black",
        "8GB/256GB/Green"
    ],

    "Laptops": [
        "8GB/512GB SSD",
        "16GB/512GB SSD",
        "16GB/1TB SSD"
    ],

    "Headphones": [
        "Black",
        "Blue",
        "White"
    ],

    "Smart Watches": [
        "Black Strap",
        "Silver Strap"
    ],

    "Shoes": [
        "Size 7",
        "Size 8",
        "Size 9",
        "Size 10"
    ],

    "Men Clothing": [
        "S",
        "M",
        "L",
        "XL"
    ],

    "Women Clothing": [
        "S",
        "M",
        "L",
        "XL"
    ],

    "Cookware": [
        "2L",
        "3L",
        "5L"
    ],

    "Kitchen Appliances": [
        "Standard"
    ],

    "Storage": [
        "500ml",
        "1L"
    ],

    "Staples": [
        "1kg",
        "5kg",
        "10kg"
    ],

    "Snacks": [
        "100g",
        "250g",
        "500g"
    ],

    "Beverages": [
        "500ml",
        "1L",
        "2L"
    ],

    "Skin Care": [
        "100ml",
        "200ml"
    ],

    "Hair Care": [
        "180ml",
        "340ml"
    ],

    "Refrigerator": [
        "260L",
        "320L",
        "420L"
    ],

    "Washing Machine": [
        "6kg",
        "8kg",
        "10kg"
    ],

    "Air Conditioner": [
        "1 Ton",
        "1.5 Ton",
        "2 Ton"
    ],

    "Office": [
        "Standard"
    ],

    "Bedroom": [
        "Queen",
        "King"
    ],

    "Fitness": [
        "5kg",
        "10kg",
        "20kg"
    ],

    "Outdoor": [
        "Standard"
    ],

    "Programming": [
        "Paperback",
        "Hardcover"
    ],

    "Business": [
        "Paperback",
        "Hardcover"
    ],

    "Educational": [
        "Standard"
    ],

    "Kids": [
        "Standard"
    ]

}


DEFAULT_VARIANTS = ["Standard"]

# ==========================================================
# JSON LOADERS
# ==========================================================

def load_catalog():
    """
    Load product catalog from JSON.
    """

    path = CONFIG_FOLDER / "product_catalog.json"

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_pricing_rules():
    """
    Load pricing rules from JSON.
    """

    path = CONFIG_FOLDER / "pricing_rules.json"

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


# ==========================================================
# ID GENERATORS
# ==========================================================

def generate_product_id(product_number):
    """
    Example:
    Product Number = 1

    Returns:
    P000001
    """

    return f"P{product_number:06d}"


def generate_sku_code(sku_number):
    """
    Example:
    SKU Number = 1

    Returns:
    SKU0000001
    """

    return f"SKU{sku_number:07d}"


# ==========================================================
# PRODUCT NAME
# ==========================================================

def build_product_name(brand, model):
    """
    Build readable product name.

    Example

    Samsung
    Galaxy M35

    →

    Samsung Galaxy M35
    """

    return f"{brand} {model}"


# ==========================================================
# VARIANT LOOKUP
# ==========================================================

def get_variants(subcategory):
    """
    Returns variant list for a subcategory.

    If not found,
    returns ["Standard"].
    """

    return VARIANTS.get(
        subcategory,
        DEFAULT_VARIANTS
    )


# ==========================================================
# RANDOM HELPERS
# ==========================================================

def random_rating():
    """
    Generates realistic rating.

    Range:
    3.5 - 4.9
    """

    return round(
        random.uniform(3.5, 4.9),
        1
    )


def random_launch_date():
    """
    Random launch date
    between 2023 and 2025.
    """

    dates = pd.date_range(
        "2023-01-01",
        "2025-12-31"
    )

    return pd.Timestamp(
        random.choice(dates)
    )


def random_active_status():
    """
    90% Active

    10% Inactive
    """

    return random.choices(
        [True, False],
        weights=[90, 10]
    )[0]

# ==========================================================
# BRAND TIERS
# ==========================================================

BRAND_TIERS = {

    "Apple": "Premium",
    "Samsung": "Premium",

    "OnePlus": "Mid",

    "Xiaomi": "Budget",
    "Redmi": "Budget",
    "Realme": "Budget",

    "Dell": "Mid",
    "HP": "Mid",
    "Lenovo": "Mid",

    "ASUS": "Premium",

    "Nike": "Premium",
    "Adidas": "Premium",
    "Puma": "Mid",

    "Boat": "Budget",
    "JBL": "Premium",
    "Sony": "Premium"

}


# ==========================================================
# PRICING HELPERS
# ==========================================================

def get_pricing_rule(pricing_rules, subcategory):
    """Return pricing configuration for a subcategory."""

    if subcategory not in pricing_rules:
        raise KeyError(
            f"Pricing rule missing for SubCategory='{subcategory}'. "
            "Check python/config/pricing_rules.json"
        )

    return pricing_rules[subcategory]



def get_brand_tier(brand):

    return BRAND_TIERS.get(
        brand,
        "Mid"
    )


def generate_base_cost(rule, brand):

    tier = get_brand_tier(brand)

    minimum = rule["cost_min"]
    maximum = rule["cost_max"]

    difference = maximum - minimum

    if tier == "Budget":

        upper = minimum + difference * 0.45

        return random.randint(
            int(minimum),
            int(upper)
        )

    elif tier == "Mid":

        lower = minimum + difference * 0.30

        upper = minimum + difference * 0.75

        return random.randint(
            int(lower),
            int(upper)
        )

    else:

        lower = minimum + difference * 0.70

        return random.randint(
            int(lower),
            int(maximum)
        )


def generate_margin(rule):

    return round(

        random.uniform(

            rule["margin_min"],
            rule["margin_max"]

        ),

        2

    )


def calculate_mrp(cost_price, margin):

    return round(

        cost_price *

        (1 + margin / 100)

    )


def generate_discount():

    discounts = [

        0,

        5,

        8,

        10,

        12,

        15,

        18,

        20

    ]

    return random.choice(discounts)


def calculate_selling_price(

        mrp,

        discount_percent

):

    return round(

        mrp *

        (1 - discount_percent / 100)

    )


def generate_weight(rule):

    return round(

        random.uniform(

            rule["weight_min"],

            rule["weight_max"]

        ),

        2

    )


# ==========================================================
# PRODUCT DIMENSION GENERATOR
# ==========================================================

def generate_product_dimension(
    catalog,
    pricing_rules,
):
    """Generate the complete Product Dimension."""

    rows = []

    product_group_number = 1
    product_number = 1
    sku_number = 1

    for category, subcategories in catalog.items():
        for subcategory, brands in subcategories.items():
            rule = get_pricing_rule(pricing_rules, subcategory)
            variants = get_variants(subcategory)

            for brand, models in brands.items():
                for model in models:

                     # One Product Group for one model
                    product_group_id = f"PG{product_group_number:06d}"


                    base_cost = generate_base_cost(rule, brand)

                    for variant in variants:

                          # One ProductID per SKU
                        product_id = generate_product_id(product_number)

                        cost_multiplier = 1.0
                        variant_lower = variant.lower()

                        if subcategory == "Smartphones":
                            if "256" in variant_lower:
                                cost_multiplier += 0.18
                            if "8gb" in variant_lower:
                                cost_multiplier += 0.08
                        elif subcategory == "Laptops":
                            if "16gb" in variant_lower:
                                cost_multiplier += 0.10
                            if "1tb" in variant_lower:
                                cost_multiplier += 0.20
                        elif subcategory == "Refrigerator":
                            if "320" in variant_lower:
                                cost_multiplier += 0.10
                            elif "420" in variant_lower:
                                cost_multiplier += 0.20
                        elif subcategory == "Washing Machine":
                            if "8kg" in variant_lower:
                                cost_multiplier += 0.08
                            elif "10kg" in variant_lower:
                                cost_multiplier += 0.18
                        elif subcategory == "Air Conditioner":
                            if "1.5" in variant_lower:
                                cost_multiplier += 0.12
                            elif "2" in variant_lower:
                                cost_multiplier += 0.22

                        adjusted_cost = round(base_cost * cost_multiplier)
                        margin = generate_margin(rule)
                        mrp = calculate_mrp(adjusted_cost, margin)

                        discount = generate_discount()
                        selling_price = calculate_selling_price(mrp, discount)

                        launch_date = random_launch_date()
                        rating = random_rating()
                        weight = generate_weight(rule)
                        active = random_active_status()

                        age_days = (
                            pd.Timestamp.today().normalize() - launch_date
                        ).days

                        if age_days <= 180:
                            lifecycle = "New Launch"
                        elif age_days <= 540:
                            lifecycle = "Growth"
                        elif age_days <= 900:
                            lifecycle = "Mature"
                        else:
                            lifecycle = "Declining"

                        rows.append(
                            {
                                "ProductGroupID": product_group_id,
                                "ProductID": product_id,
                                "SKUCode": generate_sku_code(sku_number),
                                "Category": category,
                                "SubCategory": subcategory,
                                "Brand": brand,
                                "Model": model,
                                "Variant": variant,
                                "ProductName": build_product_name(brand, model),
                                "SKUName": f"{brand} {model} {variant}",
                                "CostPrice": adjusted_cost,
                                "MarginPercent": margin,
                                "MRP": mrp,
                                "DiscountPercent": discount,
                                "SellingPrice": selling_price,
                                "GSTPercent": rule["gst"],
                                "WeightKg": weight,
                                "Rating": rating,
                                "LaunchDate": launch_date.date(),
                                "ProductLifecycle": lifecycle,
                                "ReturnWindowDays": rule["return_window"],
                                "IsActive": active,
                            }
                        )

                        sku_number += 1
                        product_group_number += 1
                        product_number += 1

                    # # increment IDs once per base model
                    # product_group_number += 1
                    # product_number += 1
                    product_group_number += 1

    # ------------------------------------------------------
    # Convert to DataFrame
    # ------------------------------------------------------

    products = pd.DataFrame(rows)



    # ------------------------------------------------------
    # Arrange Columns
    # ------------------------------------------------------

    column_order = [

        "ProductID",

        "SKUCode",

        "ProductName",

        "SKUName",

        "Category",

        "SubCategory",

        "Brand",

        "Model",

        "Variant",

        "CostPrice",

        "MarginPercent",

        "MRP",

        "DiscountPercent",

        "SellingPrice",

        "GSTPercent",

        "WeightKg",

        "Rating",

        "LaunchDate",

        "ProductLifecycle",

        "ReturnWindowDays",

        "IsActive"

    ]

    products = products[column_order]

    # ------------------------------------------------------
    # Data Types
    # ------------------------------------------------------

    products["LaunchDate"] = pd.to_datetime(
        products["LaunchDate"]
    )

    products["Rating"] = products["Rating"].round(1)

    products["MarginPercent"] = products[
        "MarginPercent"
    ].round(2)

    products["WeightKg"] = products[
        "WeightKg"
    ].round(2)

    # ------------------------------------------------------
    # Sort Products
    # ------------------------------------------------------

    products = products.sort_values(

        by=[

            "Category",

            "SubCategory",

            "Brand",

            "Model",

            "Variant"

        ]

    ).reset_index(drop=True)

    return products

# ==========================================================
# VALIDATION
# ==========================================================

def validate_product_dimension(products):
    """
    Validate generated product dimension.
    Raises an exception if any validation fails.
    """

    print("\nRunning Product Dimension Validation...")

    # ------------------------------------------------------
    # Duplicate ProductID
    # ------------------------------------------------------

    if products["ProductID"].duplicated().any():
        dup_count = int(products["ProductID"].duplicated(keep=False).sum())
        raise ValueError(
            f"Duplicate ProductID found. dup_row_count={dup_count}"
        )


    # ------------------------------------------------------
    # Duplicate SKUCode
    # ------------------------------------------------------

    if products["SKUCode"].duplicated().any():
        raise ValueError("Duplicate SKUCode found.")

    # ------------------------------------------------------
    # Null Check
    # ------------------------------------------------------

    if products.isnull().sum().sum() > 0:

        print(products.isnull().sum())

        raise ValueError("Null values found.")

    # ------------------------------------------------------
    # Selling Price
    # ------------------------------------------------------

    if (products["SellingPrice"] <= 0).any():
        raise ValueError("Selling Price must be positive.")

    # ------------------------------------------------------
    # Cost Price
    # ------------------------------------------------------

    if (products["CostPrice"] <= 0).any():
        raise ValueError("Cost Price must be positive.")

    # ------------------------------------------------------
    # MRP
    # ------------------------------------------------------

    if (products["MRP"] < products["SellingPrice"]).any():
        raise ValueError(
            "Selling Price cannot exceed MRP."
        )

    # ------------------------------------------------------
    # Rating
    # ------------------------------------------------------

    invalid_rating = (
        (products["Rating"] < 1)
        |
        (products["Rating"] > 5)
    )

    if invalid_rating.any():
        raise ValueError("Invalid Rating.")

    print("Validation Passed ✓")


# ==========================================================
# EXPORT
# ==========================================================

def export_product_dimension(products):
    """
    Export Product Dimension to CSV.
    """

    output_file = (
        OUTPUT_FOLDER
        / "dim_product.csv"
    )

    products.to_csv(
        output_file,
        index=False
    )

    print(
        f"\nCSV Generated Successfully\n{output_file}"
    )                    


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("=" * 60)
    print("Generating Product Dimension")
    print("=" * 60)

    # --------------------------------------------------
    # Load Configuration Files
    # --------------------------------------------------

    catalog = load_catalog()

    pricing_rules = load_pricing_rules()

    print("✓ Product Catalog Loaded")

    print("✓ Pricing Rules Loaded")

    # --------------------------------------------------
    # Generate Product Dimension
    # --------------------------------------------------

    products = generate_product_dimension(

        catalog,

        pricing_rules

    )

    print(

        f"✓ Generated {len(products)} Product Records"

    )

    # --------------------------------------------------
    # Validate
    # --------------------------------------------------

    validate_product_dimension(

        products

    )

    # --------------------------------------------------
    # Export
    # --------------------------------------------------

    export_product_dimension(

        products

    )
    print(products.head())
    print("\nProduct Dimension Generation Completed Successfully.")


# ==========================================================
# ENTRY POINT
# ==========================================================

if __name__ == "__main__":

    main()