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

    sales["item_name"] = sales["item_name"].str.upper()
    sales["item_name"] = sales["item_name"].str.replace(" ", "")
    sales["item_name"] = sales["item_name"].str.replace("　", "")

    flg_isnull = sales["item_price"].isnull()
    for name in list(sales.loc[flg_isnull, "item_name"].unique()):
        price = sales.loc[
            (~flg_isnull) & (sales["item_name"] == name),
            "item_price"
        ].max()
        sales["item_price"].loc[(flg_isnull) & (sales["item_name"] == name)] = price

    print(customer["顧客名"].head())
    print(sales["customer_name"].head())

    customer["顧客名"] = customer["顧客名"].str.replace(" ", "")
    customer["顧客名"] = customer["顧客名"].str.replace("　", "")

    print(customer["顧客名"].head())


if __name__ == "__main__":
    main()
