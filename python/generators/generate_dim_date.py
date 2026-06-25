import pandas as pd
import numpy as np
from datetime import datetime

def generate_date_range(start_date, end_date):
    """
    Generate one row for every calendar date.
    """

    dates = pd.date_range(start=start_date, end=end_date)

    dim_date = pd.DataFrame({
        "FullDate": dates
    })

    return dim_date

def add_calendar_attributes(dim_date):

    dim_date["DateKey"] = dim_date["FullDate"].dt.strftime("%Y%m%d").astype(int)

    dim_date["Day"] = dim_date["FullDate"].dt.day

    dim_date["Month"] = dim_date["FullDate"].dt.month

    dim_date["MonthName"] = dim_date["FullDate"].dt.month_name()

    dim_date["Year"] = dim_date["FullDate"].dt.year

    dim_date["Quarter"] = "Q" + dim_date["FullDate"].dt.quarter.astype(str)

    return dim_date

def add_business_attributes(dim_date):

    dim_date["DayName"] = dim_date["FullDate"].dt.day_name()

    dim_date["DayOfWeek"] = dim_date["FullDate"].dt.dayofweek + 1

    dim_date["WeekOfYear"] = (
        dim_date["FullDate"]
        .dt
        .isocalendar()
        .week
        .astype(int)
    )

    dim_date["IsWeekend"] = dim_date["DayOfWeek"].isin([6, 7])

    dim_date["FinancialYear"] = np.where(
        dim_date["Month"] >= 4,
        "FY"
        + dim_date["Year"].astype(str)
        + "-"
        + (dim_date["Year"] + 1).astype(str).str[-2:],

        "FY"
        + (dim_date["Year"] - 1).astype(str)
        + "-"
        + dim_date["Year"].astype(str).str[-2:]
    )

    conditions = [

        dim_date["Month"].isin([12, 1, 2]),

        dim_date["Month"].isin([3, 4, 5]),

        dim_date["Month"].isin([6, 7, 8, 9]),

        dim_date["Month"].isin([10, 11])

    ]

    seasons = [

        "Winter",

        "Summer",

        "Monsoon",

        "Festive"

    ]

    dim_date["Season"] = np.select(
        conditions,
        seasons,
        default="Unknown"
    )

    return dim_date

def validate_data(dim_date):

    assert dim_date["DateKey"].is_unique, \
        "Duplicate DateKey found"

    assert dim_date["FullDate"].is_unique, \
        "Duplicate dates found"

    assert dim_date.isnull().sum().sum() == 0, \
        "Null values found"

    print("Data Validation Passed")

    return

def export_csv(dim_date):

    dim_date.to_csv(
    "data/generated/dim_date.csv",
    index=False
)

    print("dim_date.csv exported successfully.")


def main():

    start_date = "2024-01-01"

    end_date = datetime.today().date()

    dim_date = generate_date_range(
        start_date,
        end_date
    )

    dim_date = add_calendar_attributes(
        dim_date
    )

    dim_date = add_business_attributes(
        dim_date
    )

    validate_data(
        dim_date
    )

    export_csv(
        dim_date
    )

    print(dim_date.head())

if __name__ == "__main__":
    main()