import pandas as pd
import os

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

import matplotlib.pyplot as plt


def main():
    data_dir = os.path.join("data/4/")
    log = pd.read_csv(os.path.join(data_dir, "use_log.csv"))
    customer = pd.read_csv(os.path.join(data_dir, "customer_join.csv"))

    customer_clustering = customer[["mean", "median", "max", "min", "membership_period"]]

    sc = StandardScaler()
    customer_clustering_sc = sc.fit_transform(customer_clustering)

    kmeans = KMeans(n_clusters=4, random_state=0)
    clusters = kmeans.fit(customer_clustering_sc)
    customer_clustering["cluster"] = clusters.labels_

    X = customer_clustering_sc
    pca = PCA(n_components=2)
    pca.fit(X)
    x_pca = pca.transform(X)
    pca_df = pd.DataFrame(x_pca)
    pca_df["cluster"] = customer_clustering["cluster"]

    for i in customer_clustering["cluster"].unique():
        tmp = pca_df.loc[pca_df["cluster"] == i]
        plt.scatter(tmp[0], tmp[1])

    plt.savefig(os.path.join(data_dir, "cluster.png"))


if __name__ == "__main__":
    main()
