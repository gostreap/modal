import json
import pandas as pd


def load_wals_to_glottocode():
    wals_to_glottocode = dict()
    lines = open("../data/wals_to_glottocode.csv", "r").readlines()
    for i in range(1, len(lines)):
        walscode, glottocode = lines[i].strip().split(",")
        wals_to_glottocode[walscode] = glottocode
    return wals_to_glottocode

def load_feature_list():
    return [
        feature.strip().upper()
        for feature in open("../data/feature_list.txt", "r").readlines()
    ]

def load_and_clear_wals(wals_to_glottocode):
    full_wals = json.load(open("../data/wals.json", "r"))
    wals = dict()
    for glottocode in wals_to_glottocode.values():
        walscodes = [w for w in full_wals.keys() if (w in wals_to_glottocode and wals_to_glottocode[w] == glottocode)]
        if len(walscodes) > 0:
            wals[glottocode] = full_wals[max(walscodes, key=lambda k: len(k))]
    return wals


def create_nodes_lang(wals, wals_to_glottocode):
    file = open("../data/neo4j_graph_new/nodes_lang.csv", "w")
    file.write("Name,glottocode,Genus,Family,Latitude,Longitude\n")
    for key, lang in wals.items():
        file.write(
            '"{}","{}","{}","{}",{},{}\n'.format(
                lang["language"],
                key,
                lang["genus"],
                lang["family"],
                lang["latitude"],
                lang["longitude"],
            )
        )
    file.close()


def create_nodes_features(wals, wals_to_glottocode):
    pass


def create_nodes_phonemes(phoible):
    pass


def create_edges_lang_features(wals, feature_list):
    file = open("../data/neo4j_graph_new/edges_lang_features.csv", "w")
    file.write("Source,Target,Value\n")
    for key in wals.keys():
        for feature in feature_list:
            if "_{}_num".format(feature) in wals[key]:
                file.write('"{}","{}","{}"\n'.format(key, feature, wals[key]["_{}_num".format(feature)]))
    file.close()


def create_edges_lang_phonemes(phoible, wals):
    file = open("../data/neo4j_graph_new/edges_lang_phonemes.csv", "w")
    file.write("glottocode,Phoneme,dataset\n")
    for index, row in phoible.iterrows():
        if row["Glottocode"] in wals:
            file.write('"{}","{}","{}"\n'.format(row["Glottocode"], row["Phoneme"], row["Source"]).replace('"',''))    
    file.close()


# wals to glottocode correspondance
wals_to_glottocode = load_wals_to_glottocode()

feature_list = load_feature_list()

# open Wals.json
wals = load_and_clear_wals(wals_to_glottocode)

# open phoible.csv
phoible = pd.read_csv(r"../data/phoeble.csv", low_memory=False)



# create files for neo4j graph
create_nodes_lang(wals, wals_to_glottocode)
# create_nodes_features(wals, wals_to_glottocode)
create_edges_lang_features(wals, feature_list)
# create_nodes_phonemes(phoible)
create_edges_lang_phonemes(phoible, wals)

# print(len(set(wals_to_glottocode.values())), len(wals_to_glottocode))