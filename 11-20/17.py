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

    customer["顧客名"] = customer["顧客名"].str.replace(" ", "")
    customer["顧客名"] = customer["顧客名"].str.replace("　", "")

    flg_is_serial = customer["登録日"].astype("str").str.isdigit()
    print(flg_is_serial.sum())

    from_serial = pd.to_timedelta(customer.loc[flg_is_serial, "登録日"].astype("float"), unit="D") + pd.to_datetime("1900/01/01")
    print(from_serial)

    from_string = pd.to_datetime(customer.loc[~flg_is_serial, "登録日"])
    print(from_string)

    customer["登録日"] = pd.concat([from_serial, from_string])
    print(customer)

    customer["登録年月"] = customer["登録日"].dt.strftime("%Y%m")
    rslt = customer.groupby("登録年月").count()["顧客名"]
    print(rslt)
    print(len(customer))

    flg_is_serial = customer["登録日"].astype("str").str.isdigit()
    print(flg_is_serial.sum())


if __name__ == "__main__":
    main()
