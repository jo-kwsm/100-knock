import os
import pandas as pd

def main():
    data_dir = "data/1"
    customer_path = os.path.join(data_dir, "customer_master.csv")
    item_path = os.path.join(data_dir, "item_master.csv")
    transaction_path = os.path.join(data_dir, "transaction_1.csv")
    transaction_detail_path = os.path.join(data_dir, "transaction_detail_1.csv")
    data = {
        "customer": pd.read_csv(customer_path),
        "item": pd.read_csv(item_path),
        "transaction": pd.read_csv(transaction_path),
        "transaction_detail": pd.read_csv(transaction_detail_path),
    }
    for k, v in data.items():
        print(k)
        print(v.head())

if __name__ == "__main__":
    main()
