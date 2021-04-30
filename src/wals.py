#%%
import json
import matplotlib.pyplot as plt

from lingtypology.datasets import Wals

from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import squareform

feature_list = [
    "1A",
    "2A",
    "3A",
    "4A",
    "5A",
    "6A",
    "7A",
    "8A",
    "9A",
    "10A",
    "10B",
    "11A",
    "12A",
    "13A",
    "14A",
    "15A",
    "16A",
    "17A",
    "18A",
    "19A",
    "20A",
    "21A",
    "21B",
    "22A",
    "23A",
    "24A",
    "25A",
    "25B",
    "26A",
    "27A",
    "28A",
    "29A",
    "30A",
    "31A",
    "32A",
    "33A",
    "34A",
    "35A",
    "36A",
    "37A",
    "38A",
    "39A",
    "39B",
    "40A",
    "41A",
    "42A",
    "43A",
    "44A",
    "45A",
    "46A",
    "47A",
    "48A",
    "49A",
    "50A",
    "51A",
    "52A",
    "53A",
    "54A",
    "55A",
    "56A",
    "57A",
    "58A",
    "58B",
    "59A",
    "60A",
    "61A",
    "62A",
    "63A",
    "64A",
    "65A",
    "66A",
    "67A",
    "68A",
    "69A",
    "70A",
    "71A",
    "72A",
    "73A",
    "74A",
    "75A",
    "76A",
    "77A",
    "78A",
    "79A",
    "79B",
    "80A",
    "81A",
    "81B",
    "82A",
    "83A",
    "84A",
    "85A",
    "86A",
    "87A",
    "88A",
    "89A",
    "90A",
    "90B",
    "90C",
    "90D",
    "90E",
    "90F",
    "90G",
    "91A",
    "92A",
    "93A",
    "94A",
    "95A",
    "96A",
    "97A",
    "98A",
    "99A",
    "100A",
    "101A",
    "102A",
    "103A",
    "104A",
    "105A",
    "106A",
    "107A",
    "108A",
    "108B",
    "109A",
    "109B",
    "110A",
    "111A",
    "112A",
    "113A",
    "114A",
    "115A",
    "116A",
    "117A",
    "118A",
    "119A",
    "120A",
    "121A",
    "122A",
    "123A",
    "124A",
    "125A",
    "126A",
    "127A",
    "128A",
    "129A",
    "130A",
    "130B",
    "131A",
    "132A",
    "133A",
    "134A",
    "135A",
    "136A",
    "136B",
    "137A",
    "137B",
    "138A",
    "139A",
    "140A",
    "141A",
    "142A",
    "143A",
    "143B",
    "143C",
    "143D",
    "143E",
    "143F",
    "143G",
    "144A",
    "144B",
    "144C",
    "144D",
    "144E",
    "144F",
    "144G",
    "144H",
    "144I",
    "144J",
    "144K",
    "144L",
    "144M",
    "144N",
    "144O",
    "144P",
    "144Q",
    "144R",
    "144S",
    "144T",
    "144U",
    "144V",
    "144W",
    "144X",
    "144Y",
]

#%%

features = dict()
for feature in feature_list:
    features[feature] = Wals(feature).get_df()


# %%
languages = dict()
for feature in feature_list:
    print("Feature :", feature)
    for lang in features[feature].language:
        if lang not in languages:
            languages[lang] = dict()
        languages[lang][feature] = int(
            features[feature].loc[features[feature]["language"] == lang][
                "_" + str(feature) + "_num"
            ]
        )

# %%
def save_to_json(data, path):
    out_file = open(path, 'w+')
    json.dump(data, out_file)


def load_languages_features():
    return json.load(open("../data/languages_features.json"))

# %%
def dist(lang1, lang2):
    total = 0
    same = 0
    for feature in languages[lang1]:
        if feature in languages[lang2]:
            total += 1
            if languages[lang1][feature] == languages[lang2][feature]:
                same += 1
    if total == 0:
        return 1
    return 1 - same / total

# %%
def dist_matrix(langs):
    M = []
    for l1 in langs:
        M.append([])
        for l2 in langs:
            M[-1].append(dist(l1, l2))
    return M

def get_lang_with_more_than_n_features(n):
    langs = []
    for lang in languages:
        if len(languages[lang]) > n:
            langs.append(lang)
    return langs
# %%

# %%
test = [
    "1A",
    "2A",
    "3A",
    "4A",
    "5A",
    "6A",
    "7A",
    "8A",
    "9A",
    "10A",
    "10B",
    "11A",
    "12A",
    "13A",
    "14A",
    "15A",
    "16A",
    "17A",
    "18A",
    "19A",
]

for lang in languages:
    count = 0
    total = 0
    for feature in test:
        if feature in languages["French"] and feature in languages[lang]:
            total += 1
            if languages["French"][feature] == languages[lang][feature]:
                continue
        else:
            continue
        count += 1
    if total > 5 and count / total > 0.8:
        print(lang, count, total)

# %%
# X = ["French", "German", "Spanish", "English", "Italian", "Portuguese", "Danish", "Hungarian", "Bulgarian", "Basque", "Japanese", "Korean", "Mandarin", "Zulu", "Wolof", "Lithuanian", "Latvian"]
# X = get_lang_with_more_than_n_features(140)
X = ["English", "Mandarin", "Hindi", "Spanish", "Arabic (Modern Standard)", "Bengali", "French", "Russian", "Portuguese", "Urdu", "Indonesian", "German", "Japanese", "Marathi", "Telugu", "Turkish", "Tamil", "Cantonese", "Wu", "Korean", "Vietnamese", "Hausa", "Persian", "Swahili", "Javanese", "Italian", "Thai"]
M = dist_matrix(X)
m =squareform(M)


Z = linkage(m, 'ward', optimal_ordering=True)
fig = plt.figure(figsize=(10, 25))
dn = dendrogram(Z, labels=X, orientation='right',)

Z = linkage(m, 'average', optimal_ordering=True)
fig = plt.figure(figsize=(10, 25))
dn = dendrogram(Z, labels=X, orientation='right',)
plt.show()
# %%
