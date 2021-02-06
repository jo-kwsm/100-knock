import pandas as pd
import os

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def main():
    data_dir = os.path.join("data/4/")
    log = pd.read_csv(os.path.join(data_dir, "use_log.csv"))
    customer = pd.read_csv(os.path.join(data_dir, "customer_join.csv"))

    customer_clustering = customer[["mean", "median", "max", "min", "membership_period"]]
    print(customer_clustering.head())

    sc = StandardScaler()
    customer_clustering_sc = sc.fit_transform(customer_clustering)

    kmeans = KMeans(n_clusters=4, random_state=0)
    clusters = kmeans.fit(customer_clustering_sc)
    customer_clustering["cluster"] = clusters.labels_
    print(customer_clustering["cluster"].unique())
    print(customer_clustering.head())


if __name__ == "__main__":
    main()
