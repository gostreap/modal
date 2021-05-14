# %%
import json
import matplotlib.pyplot as plt

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
                wals[row["wals_code"]]["family"] = row["language"]
                coordinates = list(row["coordinates"])
                wals[row["wals_code"]]["latitude"] = float(coordinates[0])
                wals[row["wals_code"]]["longitude"] = float(coordinates[1])
            wals[row["wals_code"]]["_" + feature + "_area"] = row[
                "_" + feature + "_area"
            ]
            wals[row["wals_code"]]["_" + feature] = row[
                "_" + feature
            ]
            wals[row["wals_code"]]["_" + feature + "_num"] = row[
                "_" + feature + "_num"
            ]
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


# %%
languages = load_languages_features()
wals = load_wals()
# languages_geo = load_languages_geo()


# %%
def dist(lang1, lang2, threshold=20):
    total = 0
    same = 0
    for feature in languages[lang1]:
        if feature in languages[lang2]:
            total += 1
            if languages[lang1][feature] == languages[lang2][feature]:
                same += 1
    if total < threshold:
        return 1
    return 1 - same / total


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
    for lang in languages:
        if len(languages[lang]) > n:
            langs.append(lang)
    return langs


# %%
# X = ["French", "German", "Spanish", "English", "Italian", "Portuguese",
# "Danish", "Hungarian", "Bulgarian", "Basque", "Japanese", "Korean",
# "Mandarin", "Zulu", "Wolof", "Lithuanian", "Latvian"]
# X = get_lang_with_more_than_n_features(40)
# X = ["English", "Mandarin", "Hindi", "Spanish", "Arabic (Modern Standard)",
# "Bengali", "French", "Russian", "Portuguese", "Urdu", "Indonesian",
# "German", "Japanese", "Marathi", "Telugu", "Turkish", "Tamil",
# "Cantonese", "Wu", "Korean", "Vietnamese", "Hausa", "Persian",
# "Swahili", "Javanese", "Italian", "Thai"]
# X = [x for x in languages]


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
def lang_dist_to_csv(langs, threshold=0.5, cluster_threshold=0.55):
    cluster = clusterize(langs, threshold=cluster_threshold)
    nodes = open("../data/Graph_lang_wals_nodes.csv", "w")
    nodes.write("Id,Label, lat, lng, cluster\n")
    for i, lang in enumerate(langs):
        nodes.write(
            "{}, {}, {}, {}, {}\n".format(
                lang,
                lang,
                languages_geo[lang]["latitude"],
                languages_geo[lang]["longitude"],
                cluster[i],
            )
        )
    nodes.close()

    M = dist_matrix(langs)
    edges = open("../data/Graph_lang_wals_edges.csv", "w")
    edges.write("Source,Target,Id,Length, Type\n")
    for i in range(len(langs)):
        for j in range(i + 1, len(langs)):
            if M[i][j] > threshold:
                continue
            edges.write(
                "{}, {}, {}, {}, {}\n".format(
                    langs[i], langs[j], i * len(langs) + j, M[i][j], "Undirected"
                )
            )
    edges.close()


# %%
