from scipy.cluster.hierarchy import dendrogram, fcluster, linkage
from scipy.spatial.distance import squareform


import lang2vec.lang2vec as l2v
import pandas as pd
import json
import matplotlib.pyplot as plt


def get_iso_to_id():
    iso_to_id = dict()
    for i, lang in enumerate(l2v.LANGUAGES):
        iso_to_id[lang] = i
    return iso_to_id


def get_dist():
    return pd.read_csv("../data/dist_l2v_syntactic.csv").to_numpy()[:,1:]


dist = get_dist()
iso_to_id = get_iso_to_id()


def load_wals():
    return json.load(open("../data/wals.json"))


euro = {
    "gae":"gla",
    "iri":"gle",
    "bre":"bre",
    "wel":"cym",
    "ice":"isl",
    "nor":"nob",
    "swe":"swe",
    "dsh":"dan",
    "eng":"eng",
    "ger":"deu",
    "dut":"nld",
    "fre":"fra",
    "ita":"ita",
    "spa":"spa",
    "ctl":"cat",
    "rom":"ron",
    "por":"por",
    "grk":"ell",
    "alb":"aln",
    "bsq":"eus",
    "fin":"fin",
    "lat":"lav",
    "est":"est",
    "lit":"lit",
    "hun":"hun",
    "pol":"pol",
    "ukr":"ukr",
    "svk":"slk",
    "slo":"slv",
    "scr":"bos",
    # "mol",
    "blr":"bel",
    "mcd":"mkd",
    "bul":"bul",
    # "bos",
    "rus":"rus",
}


def dist_matrix(langs):
    M = []
    for lang1 in langs.keys():
        M.append([])
        for lang2 in langs.keys():
            M[-1].append(dist[iso_to_id[langs[lang1]]][iso_to_id[langs[lang2]]])
    return M


def clusterize(langs, method="average", threshold=0.5):
    M = dist_matrix(langs)
    m = squareform(M)
    Z = linkage(m, method=method, optimal_ordering=True)
    cluster = fcluster(Z, threshold, criterion="distance")
    return cluster


# %%
def plot_dendrogram(langs, method="average", threshold=0.5):
    M = dist_matrix(langs)
    print(M)
    m = squareform(M)
    print(m)
    Z = linkage(m, method=method, optimal_ordering=True)
    fig = plt.figure(figsize=(10, 100))
    dn = dendrogram(Z, labels=langs, orientation="right", color_threshold=threshold)
    plt.show()


# plot_dendrogram(euro)


def write_dist_matrix(langs, threshold=20):
    wals = load_wals()
    M = dist_matrix(langs)
    dist_file = open("dist_matrix.txt", "w")
    for m in M:
        dist_file.write(" ".join(map(str, m)) + "\n")
    dist_file.close()

    label_file = open("labels.txt", "w")
    for lang in langs.keys():
        label_file.write("{}\n".format(wals[lang]["language"]))
    label_file.close()

write_dist_matrix(euro)