import os
import pandas as pd

def main():
    data_dir = "data/1"
    transaction_1_path = os.path.join(data_dir, "transaction_1.csv")
    transaction_2_path = os.path.join(data_dir, "transaction_2.csv")
    transaction_detail_1_path = os.path.join(data_dir, "transaction_detail_1.csv")
    transaction_detail_2_path = os.path.join(data_dir, "transaction_detail_2.csv")
    data = {
        "transaction_1": pd.read_csv(transaction_1_path),
        "transaction_2": pd.read_csv(transaction_2_path),
        "transaction_detail_1": pd.read_csv(transaction_detail_1_path),
        "transaction_detail_2": pd.read_csv(transaction_detail_2_path),
    }
    data["transaction"] = pd.concat([data["transaction_1"], data["transaction_2"]], ignore_index=True)
    data["transaction_detail"] = pd.concat([data["transaction_detail_1"], data["transaction_detail_2"]], ignore_index=True)
    print(len(data["transaction_detail"]))
    print(len(data["transaction"]))

    data["transaction_detail"] = pd.merge(
        data["transaction_detail"],
        data["transaction"][["transaction_id", "payment_date", "customer_id"]],
        on="transaction_id",
        how="left"
    )
    print(len(data["transaction_detail"]))

if __name__ == "__main__":
    main()
