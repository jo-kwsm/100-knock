import os
import pandas as pd


def main():
    data_dir = "data/3/"

    log = pd.read_csv(os.path.join(data_dir, "use_log.csv"))
    customer = pd.read_csv(os.path.join(data_dir, "customer_master.csv"))
    customer_class = pd.read_csv(os.path.join(data_dir, "class_master.csv"))
    campaign = pd.read_csv(os.path.join(data_dir, "campaign_master.csv"))

    print(len(log))
    print(log.head())
    print(len(customer))
    print(customer.head())
    print(len(customer_class))
    print(customer_class.head())
    print(len(campaign))
    print(campaign.head())

if __name__ == "__main__":
    main()
