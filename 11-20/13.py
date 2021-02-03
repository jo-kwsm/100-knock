import os
import pandas as pd


def main():
    data_dir = "data/2/"

    sales_path = os.path.join(data_dir, "uriage.csv")
    customer_path = os.path.join(data_dir, "kokyaku_daicho.xlsx")

    sales = pd.read_csv(sales_path)
    customer = pd.read_excel(customer_path)

    sales["purchase_date"] = pd.to_datetime(sales["purchase_date"])
    sales["purchase_month"] = sales["purchase_date"].dt.strftime("%Y%m")
    print(sales.pivot_table(index="purchase_month", columns="item_name", aggfunc="size", fill_value=0))
    print(sales.pivot_table(index="purchase_month", columns="item_name", values="item_price", aggfunc="sum", fill_value=0))


if __name__ == "__main__":
    main()
