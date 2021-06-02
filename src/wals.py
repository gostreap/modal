#" %%",
import json
import math
import numpy as np
import matplotlib.pyplot as plt

from geopy.distance import geodesic

from lingtypology.datasets import Wals

from scipy.cluster.hierarchy import dendrogram, fcluster, linkage
from scipy.spatial.distance import squareform

feature_list = [
    feature.strip().upper()
    for feature in open("../data/feature_list.txt", "r").readlines()
]

# %%
def write_wals():
    features = dict()
    for feature in feature_list:
        features[feature] = Wals(feature).get_df()

    wals = dict()
    for feature in feature_list:
        for idx, row in features[feature].iterrows():
            if row["wals_code"] not in wals:
                wals[row["wals_code"]] = dict()
                wals[row["wals_code"]]["language"] = row["language"]
                wals[row["wals_code"]]["genus"] = row["genus"]
                wals[row["wals_code"]]["family"] = row["family"]
                coordinates = list(row["coordinates"])
                wals[row["wals_code"]]["latitude"] = float(coordinates[0])
                wals[row["wals_code"]]["longitude"] = float(coordinates[1])
            wals[row["wals_code"]]["_" + feature + "_area"] = row[
                "_" + feature + "_area"
            ]
            wals[row["wals_code"]]["_" + feature] = row["_" + feature]
            wals[row["wals_code"]]["_" + feature + "_num"] = row["_" + feature + "_num"]
            wals[row["wals_code"]]["_" + feature + "_desc"] = row[
                "_" + feature + "_desc"
            ]

    wals_file = open("../data/wals.json", "w")
    json.dump(wals, wals_file)


# %%
def construct_languages():
    features = dict()
    for feature in feature_list:
        features[feature] = Wals(feature).get_df()

    languages = dict()
    languages_geo = dict()
    for feature in feature_list:
        print("Feature :", feature)
        for lang in features[feature].language:
            if lang not in languages_geo:
                coordinates = features[feature].loc[
                    features[feature]["language"] == lang
                ]["coordinates"]
                coordinates = list(coordinates)[0]
                languages_geo[lang] = dict()
                languages_geo[lang]["latitude"] = float(coordinates[0])
                languages_geo[lang]["longitude"] = float(coordinates[1])

            if lang not in languages:
                languages[lang] = dict()
            languages[lang][feature] = int(
                features[feature].loc[features[feature]["language"] == lang][
                    "_" + str(feature) + "_num"
                ]
            )
    return languages, languages_geo


# %%
def save_to_json(data, path):
    out_file = open(path, "w+")
    json.dump(data, out_file)


def load_languages_features():
    return json.load(open("../data/languages_features.json"))


def load_languages_geo():
    return json.load(open("../data/languages_geo.json"))


def load_wals():
    return json.load(open("../data/wals.json"))


def load_most_spoken():
    most_spoken = dict()
    for line in open("../data/most_spoken_wals", "r").readlines():
        a, b = line.split()
        most_spoken[a] = int(b)
    return most_spoken

# %%
NOT_FEATURES = ["language", "genus", "family", "latitude", "longitude"]

languages = load_languages_features()
wals = load_wals()

euro = [
    "gae",
    "iri",
    "bre",
    "wel",
    "ice",
    "nor",
    "swe",
    "dsh",
    "eng",
    "ger",
    "dut",
    "fre",
    "ita",
    "spa",
    "ctl",
    "rom",
    "por",
    "grk",
    "alb",
    "bsq",
    "fin",
    "lat",
    "est",
    "lit",
    "hun",
    "pol",
    "ukr",
    "svk",
    "slo",
    "scr",
    # "mol",
    "blr",
    "mcd",
    "bul",
    # "bos",
    "rus",
]

# languages_geo = load_languages_geo()


# %%
def dist(lang1, lang2, threshold=20):
    total = 0
    same = 0
    for feature in wals[lang1]:
        if feature not in NOT_FEATURES and feature in wals[lang2]:
            total += 1
            if wals[lang1][feature] == wals[lang2][feature]:
                same += 1
    if total < threshold:
        return 1
    return 1 - same / total


def geo_dist(lang1, lang2):
    return geodesic(
        (wals[lang1]["latitude"], wals[lang1]["longitude"]),
        (wals[lang2]["latitude"], wals[lang2]["longitude"]),
    )


# %%
def dist_matrix(langs, threshold=20):
    M = []
    for l1 in langs:
        M.append([])
        for l2 in langs:
            M[-1].append(dist(l1, l2, threshold=threshold))
    return M


def get_lang_with_more_than_n_features(n):
    langs = []
    for lang in wals:
        if (len(wals[lang]) - 5) / 4 > n:
            langs.append(lang)
    return langs


# %%
def plot_dendrogram(langs, method="average", threshold=0.5):
    M = dist_matrix(langs)
    m = squareform(M)
    Z = linkage(m, method=method, optimal_ordering=True)
    fig = plt.figure(figsize=(10, 100))
    dn = dendrogram(Z, labels=langs, orientation="right", color_threshold=threshold)
    plt.show()


# %%
def clusterize(langs, method="average", threshold=0.5):
    M = dist_matrix(langs)
    m = squareform(M)
    Z = linkage(m, method=method, optimal_ordering=True)
    cluster = fcluster(Z, threshold, criterion="distance")
    return cluster


# %%
def lang_dist_to_csv(langs, threshold=0.5, cluster_threshold=0.55, number_of_locutor = dict()):
    cluster = clusterize(langs, threshold=cluster_threshold)
    # cluster = [wals[lang]["family"] for lang in langs]
    nodes = open("../data/Graph_lang_wals_nodes.csv", "w")
    nodes.write("Id,Label, lat, lng, cluster, size\n")
    for i, lang in enumerate(langs):
        nodes.write(
            "{}, {}, {}, {}, {}, {}\n".format(
                lang,
                wals[lang]["language"],
                wals[lang]["latitude"],
                wals[lang]["longitude"],
                cluster[i],
                (number_of_locutor[lang] if lang in number_of_locutor else 0)
            )
        )
    nodes.close()

    M = dist_matrix(langs)
    edges = open("../data/Graph_lang_wals_edges.csv", "w")
    edges.write("Source,Target,Id,Length,Type,Weight\n")
    for i in range(len(langs)):
        for j in range(i + 1, len(langs)):
            if M[i][j] > threshold:
                continue
            edges.write(
                "{}, {}, {}, {}, {}, {}\n".format(
                    langs[i],
                    langs[j],
                    i * len(langs) + j,
                    M[i][j],
                    "Undirected",
                    1 - M[i][j],
                )
            )
    edges.close()


# %%
def write_dist_matrix(langs, threshold=20):
    M = dist_matrix(langs, threshold=threshold)
    dist_file = open("dist_matrix.txt", "w")
    for m in M:
        dist_file.write(" ".join(map(str, m)) + "\n")
    dist_file.close()

    label_file = open("labels.txt", "w")
    for lang in langs:
        label_file.write("{}\n".format(wals[lang]["language"]))
    label_file.close()


# %%
def plot_geo_lang_dist(langs):
    X = []
    Y = []
    c = 0
    for lang1 in langs:
        for lang2 in langs:
                if lang1 != lang2:
                    d = dist(lang1, lang2, threshold=100)
                    if d != 1:
                        c += 1
                        X.append(math.log(geo_dist(lang1, lang2).km))
                        Y.append(d)
    print(np.corrcoef(X,Y))
    print(c)
    plt.plot(X, Y, "x")
    plt.show()

