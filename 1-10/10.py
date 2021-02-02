import os
import pandas as pd
import matplotlib.pyplot as plt

def main():
    data_dir = "data/1"
    customer_path = os.path.join(data_dir, "customer_master.csv")
    item_path = os.path.join(data_dir, "item_master.csv")
    transaction_1_path = os.path.join(data_dir, "transaction_1.csv")
    transaction_2_path = os.path.join(data_dir, "transaction_2.csv")
    transaction_detail_1_path = os.path.join(data_dir, "transaction_detail_1.csv")
    transaction_detail_2_path = os.path.join(data_dir, "transaction_detail_2.csv")
    data = {
        "customer": pd.read_csv(customer_path),
        "item": pd.read_csv(item_path),
        "transaction_1": pd.read_csv(transaction_1_path),
        "transaction_2": pd.read_csv(transaction_2_path),
        "transaction_detail_1": pd.read_csv(transaction_detail_1_path),
        "transaction_detail_2": pd.read_csv(transaction_detail_2_path),
    }
    data["transaction"] = pd.concat([data["transaction_1"], data["transaction_2"]], ignore_index=True)
    data["transaction_detail"] = pd.concat([data["transaction_detail_1"], data["transaction_detail_2"]], ignore_index=True)

    data["transaction_detail"] = pd.merge(
        data["transaction_detail"],
        data["transaction"][["transaction_id", "payment_date", "customer_id"]],
        on="transaction_id",
        how="left",
    )
    data["transaction_detail"] = pd.merge(
        data["transaction_detail"],
        data["item"],
        on="item_id",
        how="left",
    )
    data["transaction_detail"] = pd.merge(
        data["transaction_detail"],
        data["customer"],
        on="customer_id",
        how="left",
    )
    data["transaction_detail"]["price"] = data["transaction_detail"]["item_price"] * data["transaction_detail"]["quantity"]

    data["transaction_detail"]["payment_date"] = pd.to_datetime(data["transaction_detail"]["payment_date"])
    data["transaction_detail"]["payment_month"] = data["transaction_detail"]["payment_date"].dt.strftime("%Y%m")

    graph_data = pd.pivot_table(data["transaction_detail"], index="payment_month", columns="item_name", values="price", aggfunc="sum")
    print(graph_data.head())

    data_name_list = ["PC-A", "PC-B", "PC-C", "PC-D", "PC-E"]

    for data_name in data_name_list:
        plt.plot(list(graph_data.index), graph_data[data_name], label=data_name)
    plt.legend()
    plt.savefig("./1-10/figure.png")


if __name__ == "__main__":
    main()
