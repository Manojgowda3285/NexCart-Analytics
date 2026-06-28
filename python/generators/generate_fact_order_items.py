"""
==========================================================
FACT ORDER ITEMS GENERATOR
==========================================================

Generates Fact Order Items for the
Indian E-Commerce Analytics Platform.

Grain:
One row = One Product within One Order
"""


import json
import random
from pathlib import Path

import numpy as np
import pandas as pd

# ------------------------------------------------------
# RANDOM SEED
# ------------------------------------------------------

random.seed(42)
np.random.seed(42)

# ------------------------------------------------------
# PATHS
# ------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

GENERATED_FOLDER = PROJECT_ROOT / "data" / "generated"

CONFIG_FOLDER = PROJECT_ROOT / "config"

OUTPUT_FILE = GENERATED_FOLDER / "fact_order_items.csv"

# ------------------------------------------------------
# CONFIG
# ------------------------------------------------------

TOTAL_ORDERS = 75000

MAX_ITEMS_PER_ORDER = 6

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
# LOAD BUSINESS EVENTS
# ------------------------------------------------------

with open(
    CONFIG_FOLDER / "business_events.json",
    "r",
    encoding="utf-8"
) as file:

    BUSINESS_EVENTS = json.load(file)


# ======================================================
# ID GENERATORS
# ======================================================

def generate_order_id(order_number):

    return f"ORD{order_number:08d}"


def generate_order_item_id(order_item_number):

    return f"OI{order_item_number:09d}"


# ======================================================
# BUSINESS EVENTS
# ======================================================

DEFAULT_EVENT = {
    "EventName": "Normal",
    "EventType": "Normal",
    "OrderMultiplier": 1.0,
    "DiscountMultiplier": 1.0,
    "AffectedCategory": "All",
    "AffectedWarehouse": None
}


def get_active_event(order_date):

    order_date = pd.to_datetime(order_date)

    for event in BUSINESS_EVENTS:

        start = pd.to_datetime(event["StartDate"])
        end = pd.to_datetime(event["EndDate"])

        if start <= order_date <= end:
            return event

    return DEFAULT_EVENT


# ======================================================
# CUSTOMER
# ======================================================

def choose_customer():

    return dim_customer.sample(1).iloc[0]


# ======================================================
# ORDER DATE
# ======================================================

def choose_order_date():

    return dim_date.sample(1).iloc[0]


# ======================================================
# PAYMENT
# ======================================================

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

        weights=[42, 22, 16, 8, 5, 7]

    )[0]


# ======================================================
# PRODUCTS
# ======================================================

def choose_products(item_count):

    return dim_product.sample(

        n=item_count,

        replace=False

    )


# ======================================================
# SELLER
# ======================================================

def choose_seller(category):

    eligible = dim_seller[

        dim_seller["BusinessCategory"] == category

    ]

    if len(eligible) == 0:

        return dim_seller.sample(1).iloc[0]

    return eligible.sample(1).iloc[0]


# ======================================================
# WAREHOUSE
# ======================================================

def choose_warehouse(customer_region):

    same_region = dim_warehouse[

        dim_warehouse["Region"] == customer_region

    ]

    other_region = dim_warehouse[

        dim_warehouse["Region"] != customer_region

    ]

    use_same_region = random.choices(

        [True, False],

        weights=[70, 30]

    )[0]

    if use_same_region and len(same_region) > 0:

        return same_region.sample(1).iloc[0]

    return other_region.sample(1).iloc[0]


# ======================================================
# QUANTITY
# ======================================================

def generate_quantity(category):

    rules = {

        "Electronics": [1, 2],

        "Fashion": [1, 2, 3],

        "Home & Kitchen": [1, 2],

        "Beauty": [1, 2, 3],

        "Books": [1, 2, 3],

        "Sports": [1, 2],

        "Grocery": [1, 2, 3, 4, 5]

    }

    return random.choice(

        rules.get(category, [1])

    )


# ======================================================
# SHIPPING
# ======================================================

def generate_shipping_charge(category):

    shipping = {

        "Electronics": (120, 350),

        "Fashion": (60, 150),

        "Home & Kitchen": (80, 220),

        "Beauty": (40, 100),

        "Books": (40, 80),

        "Sports": (80, 180),

        "Grocery": (20, 70)

    }

    minimum, maximum = shipping.get(

        category,

        (50, 100)

    )

    return random.randint(

        minimum,

        maximum

    )
# ======================================================
# DISCOUNT
# ======================================================

def generate_discount_percent(category, event):

    rules = {

        "Electronics": (5, 20),

        "Fashion": (20, 50),

        "Home & Kitchen": (10, 30),

        "Beauty": (10, 30),

        "Books": (5, 15),

        "Sports": (10, 25),

        "Grocery": (0, 10)

    }

    minimum, maximum = rules.get(category, (5, 15))

    discount = random.uniform(

        minimum,

        maximum

    )

    discount *= event["DiscountMultiplier"]

    discount = min(discount, 70)

    return round(discount, 2)


# ======================================================
# PRICE CALCULATOR
# ======================================================

def calculate_order_amount(

    unit_price,

    quantity,

    gst_percent,

    shipping_charge,

    category,

    event

):

    gross_amount = unit_price * quantity

    discount_percent = generate_discount_percent(

        category,

        event

    )

    discount_amount = round(

        gross_amount * discount_percent / 100,

        2

    )

    taxable_amount = round(

        gross_amount - discount_amount,

        2

    )

    tax_amount = round(

        taxable_amount * gst_percent / 100,

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


# ======================================================
# BUILD FACT ROW
# ======================================================

def build_order_row(

    order_item_id,

    order_id,

    order_date,

    order_date_key,

    customer_id,

    payment_method,

    product,

    seller,

    warehouse,

    quantity,

    shipping_charge,

    event

  

):

    pricing = calculate_order_amount(

        unit_price=product["SellingPrice"],

        quantity=quantity,

        gst_percent=product["GSTPercent"],

        shipping_charge=shipping_charge,

        category=product["Category"],

        event=event

    )

    lifecycle = generate_order_lifecycle(

    order_date=order_date,

    category=product["Category"],

    event=event)

    delivery_date_key = None

    if lifecycle["DeliveryDate"] is not None:

        delivery_date_key = int(

            lifecycle["DeliveryDate"]

            .strftime("%Y%m%d")

        )

    return {

        "OrderItemID": order_item_id,

        "OrderID": order_id,

        "OrderDateKey": order_date_key,

        "DeliveryDateKey": delivery_date_key,

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

        "TotalAmount": pricing["TotalAmount"],

        "OrderStatus": lifecycle["OrderStatus"],

        "DeliveryDays": lifecycle["DeliveryDays"],

        "IsReturned": lifecycle["IsReturned"],

        "CustomerRating": lifecycle["CustomerRating"],

        "EventName": event["EventName"],

        "EventType": event["EventType"]

    }

# ======================================================
# ORDER LIFECYCLE
# ======================================================

def generate_order_lifecycle(order_date, category, event):

    # ----------------------------
    # Cancellation
    # ----------------------------

    cancellation_probability = 0.05

    if event["EventType"] == "Operations":

        cancellation_probability = 0.08

    if random.random() < cancellation_probability:

        return {

            "OrderStatus": "Cancelled",

            "DeliveryDate": None,

            "DeliveryDays": None,

            "IsReturned": False,

            "CustomerRating": None

        }

    # ----------------------------
    # Delivery Days
    # ----------------------------

    delivery_days = random.randint(2, 7)

    if event["EventType"] == "Operations":

        delivery_days += 3

    delivery_date = (

        pd.to_datetime(order_date)

        + pd.Timedelta(days=delivery_days)

    )

    # ----------------------------
    # Return Probability
    # ----------------------------

    return_probability = {

        "Electronics": 0.06,

        "Fashion": 0.15,

        "Home & Kitchen": 0.08,

        "Beauty": 0.07,

        "Books": 0.03,

        "Sports": 0.05,

        "Grocery": 0.01

    }

    is_returned = (

        random.random()

        <

        return_probability.get(category, 0.05)

    )

    status = "Returned" if is_returned else "Delivered"

    # ----------------------------
    # Customer Rating
    # ----------------------------

    if status == "Returned":

        rating = round(

            random.uniform(1.5, 3.5),

            1

        )

    else:

        rating = round(

            random.uniform(3.8, 5.0),

            1

        )

    return {

        "OrderStatus": status,

        "DeliveryDate": delivery_date,

        "DeliveryDays": delivery_days,

        "IsReturned": is_returned,

        "CustomerRating": rating

    }

# ======================================================
# FACT ORDER ITEMS GENERATOR
# ======================================================

def generate_fact_order_items():

    rows = []

    order_item_number = 1

    for order_number in range(1, TOTAL_ORDERS + 1):

        if order_number % 2000 == 0:
            print(f"Generated {order_number:,} orders...")

        # ---------------------------------------------
        # Order Information
        # ---------------------------------------------

        order_id = generate_order_id(order_number)

        order_date = choose_order_date()

        order_date_key = order_date["DateKey"]

        event = get_active_event(

            order_date["FullDate"]

        )

        customer = choose_customer()

        customer_id = customer["CustomerID"]

        customer_region = customer["Region"]

        payment_method = choose_payment_method()

        # ---------------------------------------------
        # Number of Items
        # ---------------------------------------------

        item_count = random.choices(

            [1, 2, 3, 4, 5, 6],

            weights=[60, 25, 8, 4, 2, 1]

        )[0]

        # Increase basket size during major events

        if event["OrderMultiplier"] > 1:

            if random.random() < 0.60:

                item_count = min(

                    item_count + 1,

                    MAX_ITEMS_PER_ORDER

                )

        # ---------------------------------------------
        # Products
        # ---------------------------------------------

        selected_products = choose_products(

            item_count

        )

        # ---------------------------------------------
        # One Row Per Product
        # ---------------------------------------------

        for _, product in selected_products.iterrows():

            seller = choose_seller(

                product["Category"]

            )

            warehouse = choose_warehouse(

                customer_region

            )

            quantity = generate_quantity(

                product["Category"]

            )

            shipping_charge = generate_shipping_charge(

                product["Category"]

            )

            row = build_order_row(

                order_item_id=generate_order_item_id(
                    order_item_number
                ),

                order_id=order_id,

                order_date_key=order_date_key,
                
                order_date = order_date["FullDate"],
              
                customer_id=customer_id,

                payment_method=payment_method,

                product=product,

                seller=seller,

                warehouse=warehouse,

                quantity=quantity,

                shipping_charge=shipping_charge,

                event=event

            )

            rows.append(

                row

            )

            order_item_number += 1

    fact_orders = pd.DataFrame(

        rows

    )

    return fact_orders


# ======================================================
# VALIDATION
# ======================================================

def validate_data(fact_orders):

    print("\nRunning validations...")

    # -----------------------------------------
    # Duplicate OrderItemID
    # -----------------------------------------

    duplicate_count = fact_orders["OrderItemID"].duplicated().sum()

    if duplicate_count > 0:

        raise ValueError(

            f"Duplicate OrderItemID found : {duplicate_count}"

        )

    # -----------------------------------------
    # Null Check
    # -----------------------------------------

    required_columns = [

        "OrderItemID",

        "OrderID",

        "CustomerID",

        "ProductID",

        "SellerID",

        "WarehouseID"

    ]

    for column in required_columns:

        if fact_orders[column].isnull().sum() > 0:

            raise ValueError(

                f"Null values found in {column}"

            )

    # -----------------------------------------
    # Price Validation
    # -----------------------------------------

    if (fact_orders["TotalAmount"] <= 0).any():

        raise ValueError(

            "Invalid TotalAmount found."

        )

    print("All validations passed.")

# ======================================================
# EXPORT
# ======================================================

def export_csv(fact_orders):

    OUTPUT_FILE.parent.mkdir(

        parents=True,

        exist_ok=True

    )

    fact_orders.to_csv(

        OUTPUT_FILE,

        index=False

    )

    print(

        f"\nSaved : {OUTPUT_FILE}"

    )

# ======================================================
# MAIN
# ======================================================

def main():

    print(

        "\nGenerating Fact Order Items...\n"

    )

    fact_orders = generate_fact_order_items()

    

    validate_data(

        fact_orders

    )

    export_csv(

        fact_orders

    )

    print(

        "\nFact Order Items Generated Successfully."

    )


if __name__ == "__main__":

    main()





