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

    print(len(sales["item_name"].unique()))

    sales["item_name"] = sales["item_name"].str.upper()
    sales["item_name"] = sales["item_name"].str.replace(" ", "")
    sales["item_name"] = sales["item_name"].str.replace("　", "")

    print(sales["item_name"].unique())
    print(len(sales["item_name"].unique()))


if __name__ == "__main__":
    main()
