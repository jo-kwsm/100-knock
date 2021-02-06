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

    customer_clustering = pd.concat([customer_clustering, customer], axis=1)

    log["usedate"] = pd.to_datetime(log["usedate"])
    log["年月"] = log["usedate"].dt.strftime("%Y%m")
    log_months = log.groupby(["年月", "customer_id"], as_index=False).count()
    log_months.rename(columns={"log_id":"count"}, inplace=True)
    del log_months["usedate"]
    print(log_months.head())

    year_months = list(log_months["年月"].unique())
    predict_data = pd.DataFrame()
    for i in range(6, len(year_months)):
        tmp = log_months.loc[log_months["年月"] == year_months[i]]
        tmp.rename(columns={"count":"count_pred"}, inplace=True)
        for j in range(1, 7):
            tmp_before = log_months.loc[log_months["年月"] == year_months[i-j]]
            del tmp_before["年月"]
            tmp_before.rename(columns={"count":"count_{}".format(j-1)}, inplace=True)
            tmp = pd.merge(tmp, tmp_before, on="customer_id", how="left")
        predict_data = pd.concat([predict_data, tmp], ignore_index=True)
    print(predict_data.head())

    predict_data = predict_data.dropna()
    predict_data = predict_data.reset_index(drop=True)
    print(predict_data.head())


if __name__ == "__main__":
    main()
