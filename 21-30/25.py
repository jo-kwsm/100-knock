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

    log["usedate"] = pd.to_datetime(log["usedate"])
    log["年月"] = log["usedate"].dt.strftime("%Y%m")
    log_months = log.groupby(["年月", "customer_id"], as_index=False).count()
    log_months.rename(columns={"log_id": "count"}, inplace=True)
    del log_months["usedate"]
    print(log_months.head())

    log_customer = log_months.groupby("customer_id").agg(["mean", "median", "max", "min"])["count"]
    log_customer = log_customer.reset_index(drop=False)
    print(log_customer.head())


if __name__ == "__main__":
    main()
