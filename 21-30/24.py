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

    customer_join["start_date"] = pd.to_datetime(customer_join["start_date"])
    customer_start = customer_join.loc[customer_join["start_date"] > pd.to_datetime("20180101")]

    customer_join["end_date"] = pd.to_datetime(customer_join["end_date"])
    customer_newer = customer_join.loc[(customer_join["end_date"] >= pd.to_datetime("20190331")) | (customer_join["end_date"].isna())]
    print(len(customer_newer))
    print(customer_newer["end_date"].unique())
    print(customer_newer.groupby("class_name").count()["customer_id"])
    print(customer_newer.groupby("campaign_name").count()["customer_id"])
    print(customer_newer.groupby("gender").count()["customer_id"])


if __name__ == "__main__":
    main()
