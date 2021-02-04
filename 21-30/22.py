import os
import pandas as pd


def main():
    data_dir = "data/3/"

    log = pd.read_csv(os.path.join(data_dir, "use_log.csv"))
    customer = pd.read_csv(os.path.join(data_dir, "customer_master.csv"))
    customer_class = pd.read_csv(os.path.join(data_dir, "class_master.csv"))
    campaign = pd.read_csv(os.path.join(data_dir, "campaign_master.csv"))

    customer_join = pd.merge(customer, customer_class, on="class", how="left")
    customer_join = pd.merge(customer_join, campaign, on="campaign_id", how="left")

    print(customer_join.head())


if __name__ == "__main__":
    main()
