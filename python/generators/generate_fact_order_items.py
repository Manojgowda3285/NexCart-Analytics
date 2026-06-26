"""
==========================================================
FACT ORDER ITEMS GENERATOR
==========================================================

Generates Fact Order Items for the
Indian E-Commerce Analytics Platform.

Grain:
One row = One Product within One Order
"""

import random
from pathlib import Path

import numpy as np
import pandas as pd

random.seed(42)
np.random.seed(42)

# ------------------------------------------------------
# PATHS
# ------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

GENERATED_FOLDER = PROJECT_ROOT / "data" / "generated"

OUTPUT_FOLDER = GENERATED_FOLDER

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------
# CONFIG
# ------------------------------------------------------

TOTAL_ORDERS = 75000

MAX_ITEMS_PER_ORDER = 4

# ------------------------------------------------------
# LOAD DIMENSIONS
# ------------------------------------------------------

dim_date = pd.read_csv(
    GENERATED_FOLDER / "dim_date.csv"
)

dim_customer = pd.read_csv(
    GENERATED_FOLDER / "dim_customer.csv"
)

dim_product = pd.read_csv(
    GENERATED_FOLDER / "dim_product.csv"
)

dim_seller = pd.read_csv(
    GENERATED_FOLDER / "dim_seller.csv"
)

dim_warehouse = pd.read_csv(
    GENERATED_FOLDER / "dim_warehouse.csv"
)

# ------------------------------------------------------
# LOOKUPS
# ------------------------------------------------------

customer_lookup = dim_customer.set_index("CustomerID")

product_lookup = dim_product.set_index("ProductID")

seller_lookup = dim_seller.set_index("SellerID")

warehouse_lookup = dim_warehouse.set_index("WarehouseID")

# ------------------------------------------------------
# ID HELPERS
# ------------------------------------------------------

def generate_order_id(number):

    return f"ORD{number:08d}"


def generate_order_item_id(number):

    return f"OI{number:09d}"

# ------------------------------------------------------
# HELPER FUNCTIONS
# ------------------------------------------------------

def choose_order_date():

    return dim_date.sample(1).iloc[0]


def choose_customer():

    return dim_customer.sample(1).iloc[0]


def choose_products(item_count):

    return dim_product.sample(
        n=item_count,
        replace=False
    )


def choose_payment_method():

    return random.choices(

        [
            "UPI",
            "Credit Card",
            "Debit Card",
            "Net Banking",
            "Wallet",
            "Cash on Delivery"
        ],

        weights=[42,22,16,8,5,7]

    )[0]


# ------------------------------------------------------
# GENERATE FACT ORDER ITEMS
# ------------------------------------------------------

def generate_fact_order_items():

    rows = []

    order_item_number = 1

    for order_number in range(1, TOTAL_ORDERS + 1):

        # -------------------------------------------------
        # Order Level Information
        # -------------------------------------------------

        order_id = generate_order_id(order_number)

        customer = choose_customer()

        customer_id = customer["CustomerID"]

        customer_region = customer["Region"]

        order_date = choose_order_date()

        order_date_key = order_date["DateKey"]

        payment_method = choose_payment_method()

        # -------------------------------------------------
        # Number of Items in this Order
        # -------------------------------------------------

        item_count = random.choices(

            [1, 2, 3, 4, 5, 6],

            weights=[60, 25, 8, 4, 2, 1]

        )[0]

        selected_products = choose_products(item_count)

        # -------------------------------------------------
        # One Row Per Product
        # -------------------------------------------------

        for _, product in selected_products.iterrows():

            # ---------------------------------------------
            # Seller
            # ---------------------------------------------

            seller = choose_seller(

                product["Category"]

            )

            # ---------------------------------------------
            # Warehouse
            # ---------------------------------------------

            warehouse = choose_warehouse(

                customer_region

            )

            # ---------------------------------------------
            # Quantity
            # ---------------------------------------------

            quantity = generate_quantity(

                product["Category"]

            )

            # ---------------------------------------------
            # Shipping
            # ---------------------------------------------

            shipping_charge = generate_shipping_charge(

                product["Category"]

            )

            # ---------------------------------------------
            # Create Fact Row
            # ---------------------------------------------

            rows.append(

    build_order_row(

        order_item_id=generate_order_item_id(order_item_number),

        order_id=order_id,

        order_date_key=order_date_key,

        customer_id=customer_id,

        payment_method=payment_method,

        product=product,

        seller=seller,

        warehouse=warehouse,

        quantity=quantity,

        shipping_charge=shipping_charge

    ))    
            order_item_number += 1

    fact_orders = pd.DataFrame(rows)

    return fact_orders

# ------------------------------------------------------
# HELPER FUNCTIONS
# ------------------------------------------------------

def choose_seller(product_category):

    eligible = dim_seller[
        dim_seller["BusinessCategory"] == product_category
    ]

    return eligible.sample(1).iloc[0]


def choose_warehouse(customer_region):

    same_region = dim_warehouse[
        dim_warehouse["Region"] == customer_region
    ]

    other_region = dim_warehouse[
        dim_warehouse["Region"] != customer_region
    ]

    use_same_region = random.choices(

        [True, False],

        weights=[70,30]

    )[0]

    if use_same_region and len(same_region) > 0:

        return same_region.sample(1).iloc[0]

    return other_region.sample(1).iloc[0]


def generate_quantity(category):

    if category == "Electronics":

        return random.choices(

            [1,2],

            weights=[90,10]

        )[0]

    elif category == "Grocery":

        return random.randint(1,5)

    elif category == "Books":

        return random.randint(1,3)

    else:

        return random.randint(1,2)


def generate_shipping_charge(category):

    shipping = {

        "Electronics": (120,350),

        "Fashion": (60,150),

        "Home & Kitchen": (80,220),

        "Beauty": (40,100),

        "Books": (40,80),

        "Sports": (80,180),

        "Grocery": (20,70)

    }

    minimum, maximum = shipping[category]

    return random.randint(

        minimum,

        maximum

    )

# ------------------------------------------------------
# DISCOUNT
# ------------------------------------------------------

def generate_discount_percent(category):

    rules = {

        "Electronics": (5,20),

        "Fashion": (20,50),

        "Home & Kitchen": (10,30),

        "Beauty": (10,30),

        "Books": (5,15),

        "Sports": (10,25),

        "Grocery": (0,10)

    }

    minimum, maximum = rules[category]

    return round(

        random.uniform(

            minimum,

            maximum

        ),

        2

    )


# ------------------------------------------------------
# PRICE CALCULATOR
# ------------------------------------------------------

def calculate_order_amount(

    unit_price,

    quantity,

    gst_percent,

    shipping_charge,

    category

):

    gross_amount = unit_price * quantity

    discount_percent = generate_discount_percent(

        category

    )

    discount_amount = round(

        gross_amount *

        discount_percent / 100,

        2

    )

    taxable_amount = round(

        gross_amount -

        discount_amount,

        2

    )

    tax_amount = round(

        taxable_amount *

        gst_percent / 100,

        2

    )

    total_amount = round(

        taxable_amount +

        tax_amount +

        shipping_charge,

        2

    )

    return {

        "GrossAmount": gross_amount,

        "DiscountPercent": discount_percent,

        "DiscountAmount": discount_amount,

        "TaxAmount": tax_amount,

        "TotalAmount": total_amount

    }


# ------------------------------------------------------
# BUILD ORDER ROW
# ------------------------------------------------------

def build_order_row(

    order_item_id,

    order_id,

    order_date_key,

    customer_id,

    payment_method,

    product,

    seller,

    warehouse,

    quantity,

    shipping_charge

):

    pricing = calculate_order_amount(

        unit_price=product["SellingPrice"],

        quantity=quantity,

        gst_percent=product["GSTPercent"],

        shipping_charge=shipping_charge,

        category=product["Category"]

    )

    return {

        "OrderItemID": order_item_id,

        "OrderID": order_id,

        "OrderDateKey": order_date_key,

        "CustomerID": customer_id,

        "ProductID": product["ProductID"],

        "SellerID": seller["SellerID"],

        "WarehouseID": warehouse["WarehouseID"],

        "PaymentMethod": payment_method,

        "Quantity": quantity,

        "UnitPrice": product["SellingPrice"],

        "UnitCost": product["CostPrice"],

        "GrossAmount": pricing["GrossAmount"],

        "DiscountPercent": pricing["DiscountPercent"],

        "DiscountAmount": pricing["DiscountAmount"],

        "GSTPercent": product["GSTPercent"],

        "TaxAmount": pricing["TaxAmount"],

        "ShippingCharge": shipping_charge,

        "TotalAmount": pricing["TotalAmount"]

    }