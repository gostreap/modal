#from lingtypology.datasets import Wals


import json
import pandas as pd
import sys




feature_list = [
    feature.strip().upper()
    for feature in open("../data/feature_list.txt", "r").readlines()
]

# open Wals.json
file_wals = open("../data/wals.json", )
wals = json.load(file_wals)

# open phoible.csv
df_phoeble = pd.read_csv(r"../data/phoeble.csv", low_memory = False)

# open languoid.tab for correspondance ISO to Wals code
df_wals = pd.read_csv(r"../data/correspondanceWals.csv", encoding='latin-1',low_memory = False)

keys_list = list(df_wals["WALS code"])
values_list = list(df_wals["ISO 639-3"])

zip_iterator_walsToISO = zip(keys_list, values_list)
walsToISO = dict(zip_iterator_walsToISO)

zip_iterator_ISOToWals = zip(values_list, keys_list)
ISOToWals = dict(zip_iterator_ISOToWals)

json.dump(ISOToWals, open("../data/iso3_to_wals.json", "w"))


# languages_walscodes = [*wals]
# languages_walsISO = []
# for code in languages_walscodes:
#     if code in walsToISO:
#         languages_walsISO.append(walsToISO[code])

# iso_phoeble = df_phoeble["ISO6393"]
# name_phoeble = df_phoeble["LanguageName"]

# # creating dict for lang -> ISO and ISO -> lang
# zip_iterator_langToIso = zip(name_phoeble, iso_phoeble)
# langToIso = dict(zip_iterator_langToIso)

# zip_iterator_isoToLang = zip(iso_phoeble, name_phoeble)
# isoToLang = dict(zip_iterator_isoToLang)

# languages = list(set(languages_walsISO).intersection(iso_phoeble))

# new_languages_walscodes = []
# for code in languages_walscodes:
#     if code in walsToISO:
#         if walsToISO[code] not in languages:
#             new_languages_walscodes.append(code)

# wals_languages = []
# for lang in new_languages_walscodes:
#     wals_languages.append(wals[lang]["language"])

# arr = list(set(wals_languages).intersection(name_phoeble))
# arr_iso = [langToIso[elem] for elem in arr]
# languages = languages + arr_iso

# arr = set(arr)
# for lang in new_languages_walscodes:
#     if wals[lang]["language"] in arr:
#         ISOToWals[langToIso[wals[lang]["language"]]] = lang
#         walsToISO[lang] = langToIso[wals[lang]["language"]]

# languages.sort()


# print(len(languages))

# # construction du nodes_lang.csv pour Neo4J

# dataframe = pd.read_csv("../data/correspondanceWals.csv")

# dataframe.drop(['WALS code'], axis=1, inplace=True)

# languages_set = set(languages)
# to_remove = []
# for i, row in dataframe.iterrows():
#     if row["ISO 639-3"] not in languages_set:
#         to_remove.append(i)

# dataframe.drop(to_remove, axis=0, inplace=True)

# dataframe.to_csv("../data/nodes_lang.csv", index=False)

## FEATURES


# wals_edges = open("../data/wals_edges.csv", "w")
# wals_edges.write("Source, Target, Value\n")
#
# language_features = json.load(open("../data/languages_features.json"))
#
# for lang in languages:
#     for feature, value in language_features[wals[ISOToWals[lang]]["language"]].items():
#         wals_edges.write("{}, {}, {}\n".format(lang, feature, value))

#PHONEMS
# phonems_phoible = pd.read_csv("../data/phonem.csv")
# properties_phoible = pd.read_csv("../data/phoeble.csv",low_memory = False)
#
# dic_phonem_properties = dict()
# for i, row in properties_phoible.iterrows():
#     if row["Phoneme"] not in dic_phonem_properties:
#         dic_phonem_properties[row["Phoneme"]] = dict()
#         for (columnName, columnData) in properties_phoible.iteritems():
#             if columnName in ["tone" , "stress", "syllabic","short","long","consonantal","sonorant","continuant","delayedRelease",
#                 "approximant","tap","trill","nasal","lateral","labial","round","labiodental","coronal","anterior","distributed","strident",
#                 "dorsal","high","low","front","back","tense","retractedTongueRoot","advancedTongueRoot","periodicGlottalSource",
#                 "epilaryngealSource","spreadGlottis","constrictedGlottis","fortis","raisedLarynxEjective","loweredLarynxImplosive","click"]:
#                 dic_phonem_properties[row["Phoneme"]][columnName] = row[columnName]

# phonem_file = open("../data/phonem.json", "w")
# json.dump(dic_phonem_properties, phonem_file)

# # open phonem.json
# file_phoneme = open("../data/phonem.json", )
# dic_phoneme = json.load(file_phoneme)
#
# phonems_phoible = pd.read_csv("../data/phonem.csv")
# properties_phoible = pd.read_csv("../data/phoeble.csv",low_memory = False)
#
#
# list_prop = ["tone" , "stress", "syllabic","short","long","consonantal","sonorant","continuant","delayedRelease",
#                  "approximant","tap","trill","nasal","lateral","labial","round","labiodental","coronal","anterior","distributed","strident",
#                  "dorsal","high","low","front","back","tense","retractedTongueRoot","advancedTongueRoot","periodicGlottalSource",
#                  "epilaryngealSource","spreadGlottis","constrictedGlottis","fortis","raisedLarynxEjective","loweredLarynxImplosive","click"]
#
# for i in range(8,8+len(list_prop)):
#     phonems_phoible.insert(i, list_prop[i-8], "test")
#
# to_remove = []
# for i, row in phonems_phoible.iterrows():
#     for attr in list_prop:
#         if row["name"] in dic_phoneme:
#             phonems_phoible.loc[i,attr] = str(dic_phoneme[row["name"]][attr])
#         else:
#             to_remove.append(i)
#
# phonems_phoible.drop(to_remove, axis=0, inplace=True)
#
# phonems_phoible.to_csv("../data/phonemes_nodes.csv", index=False)
#
# # PHOENEMES EDGES
# # dataframe = pd.read_csv("../data/phoible_edges.csv")
# #
# # languages_set = set(languages)
# # to_remove = []
# # for i, row in dataframe.iterrows():
# #     if row["ISO6393"] not in languages_set:
# #         to_remove.append(i)
# #
# # dataframe.drop(to_remove, axis=0, inplace=True)
# #
# # dataframe.to_csv("../data/phoible_edges.csv", index=False)

