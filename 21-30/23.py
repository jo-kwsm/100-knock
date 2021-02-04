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

    print(customer_join.groupby("class_name").count()["customer_id"])
    print(customer_join.groupby("campaign_name").count()["customer_id"])
    print(customer_join.groupby("gender").count()["customer_id"])
    print(customer_join.groupby("is_deleted").count()["customer_id"])

    customer_join["start_date"] = pd.to_datetime(customer_join["start_date"])
    customer_start = customer_join.loc[customer_join["start_date"] > pd.to_datetime("20180101")]
    print(len(customer_start))


if __name__ == "__main__":
    main()
