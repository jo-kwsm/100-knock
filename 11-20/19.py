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
    from_serial = pd.to_timedelta(customer.loc[flg_is_serial, "登録日"].astype("float"), unit="D") + pd.to_datetime("1900/01/01")
    from_string = pd.to_datetime(customer.loc[~flg_is_serial, "登録日"])
    customer["登録日"] = pd.concat([from_serial, from_string])

    customer["登録年月"] = customer["登録日"].dt.strftime("%Y%m")

    join_data = pd.merge(sales, customer, left_on="customer_name", right_on="顧客名", how="left")
    join_data = join_data.drop("customer_name", axis=1)
    
    dump_data = join_data[[
        "purchase_date",
        "purchase_month",
        "item_name",
        "item_price",
        "顧客名",
        "かな",
        "地域",
        "メールアドレス",
        "登録日"
    ]]
    print(dump_data)
    dump_data.to_csv(os.path.join(data_dir, "dump_data.csv"), index=False)


if __name__ == "__main__":
    main()
