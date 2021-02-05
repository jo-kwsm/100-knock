import os
import pandas as pd

from dateutil.relativedelta import relativedelta


def main():
    data_dir = "data/3/"

    log = pd.read_csv(os.path.join(data_dir, "use_log.csv"))
    customer = pd.read_csv(os.path.join(data_dir, "customer_master.csv"))
    customer_class = pd.read_csv(os.path.join(data_dir, "class_master.csv"))
    campaign = pd.read_csv(os.path.join(data_dir, "campaign_master.csv"))

    customer_join = pd.merge(customer, customer_class, on="class", how="left")
    customer_join = pd.merge(customer_join, campaign, on="campaign_id", how="left")

    customer_join["start_date"] = pd.to_datetime(customer_join["start_date"])

    customer_join["end_date"] = pd.to_datetime(customer_join["end_date"])
    customer_newer = customer_join.loc[(customer_join["end_date"] >= pd.to_datetime("20190331")) | (customer_join["end_date"].isna())]

    log["usedate"] = pd.to_datetime(log["usedate"])
    log["年月"] = log["usedate"].dt.strftime("%Y%m")
    log_months = log.groupby(["年月", "customer_id"], as_index=False).count()
    log_months.rename(columns={"log_id": "count"}, inplace=True)
    del log_months["usedate"]

    log_customer = log_months.groupby("customer_id").agg(["mean", "median", "max", "min"])["count"]
    log_customer = log_customer.reset_index(drop=False)

    log["weekday"] = log["usedate"].dt.weekday
    log_weekday = log.groupby(["customer_id", "年月", "weekday"], as_index = False).count()[["customer_id", "年月", "weekday", "log_id"]]
    log_weekday.rename(columns={"log_id":"count"}, inplace=True)

    log_weekday = log_weekday.groupby("customer_id", as_index=False).max()[["customer_id", "count"]]
    log_weekday["routine_flg"] = 0
    log_weekday["routine_flg"] = log_weekday["routine_flg"].where(log_weekday["count"] < 4, 1)

    customer_join = pd.merge(customer_join, log_customer, on="customer_id", how="left")
    customer_join = pd.merge(customer_join, log_weekday[["customer_id", "routine_flg"]], on="customer_id", how="left")

    customer_join["calc_date"] = customer_join["end_date"]
    customer_join["calc_date"] = customer_join["calc_date"].fillna(pd.to_datetime("20190430"))
    customer_join["membership_period"] = 0
    for i in range(len(customer_join)):
        delta = relativedelta(customer_join["calc_date"].iloc[i], customer_join["start_date"].iloc[i])
        customer_join["membership_period"].iloc[i] = delta.years*12 + delta.months
    
    print(customer_join.head())



if __name__ == "__main__":
    main()
