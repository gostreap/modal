import pandas as pd
import sys

from matplotlib import pyplot as plt

from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster

sys.setrecursionlimit(100000)

df = pd.read_csv("../data/dist_l2v_syntactic.csv")
dist = df.to_numpy()
dist = dist[:, 1:]

condense_dist = squareform(dist)

Z = linkage(condense_dist, "average")
# fig = plt.figure(figsize=(25, 10))
# dn = dendrogram(Z)

# plt.show()

k = 3
T = fcluster(Z, k, "maxclust")

# calculate labels
labels = list("" for i in range(len(dist)))
for i in range(len(dist)):
    labels[i] = str(i) + "," + str(T[i])

# calculate color threshold
ct = Z[-(k - 1), 2]

# plot
P = dendrogram(Z, labels=labels, color_threshold=ct)
plt.show()
