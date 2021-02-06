import pandas as pd
import os


def main():
    data_dir = os.path.join("data/4/")
    log = pd.read_csv(os.path.join(data_dir, "use_log.csv"))
    customer = pd.read_csv(os.path.join(data_dir, "customer_join.csv"))
    print(log.isnull().sum())
    print(customer.isnull().sum())


if __name__ == "__main__":
    main()
