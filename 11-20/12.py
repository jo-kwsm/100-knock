import os
import pandas as pd


def main():
    data_dir = "data/2/"

    sales_path = os.path.join(data_dir, "uriage.csv")
    customer_path = os.path.join(data_dir, "kokyaku_daicho.xlsx")

    sales = pd.read_csv(sales_path)
    customer = pd.read_excel(customer_path)

    print(sales["item_name"].head())
    print(sales["item_price"].head())


if __name__ == "__main__":
    main()
