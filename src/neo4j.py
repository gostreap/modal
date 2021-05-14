import json
import pandas as pd
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


languages_walscodes = [*wals]
languages_walsISO = []
for code in languages_walscodes:
    if code in walsToISO:
        languages_walsISO.append(walsToISO[code])

iso_phoeble = df_phoeble["ISO6393"]
name_phoeble = df_phoeble["LanguageName"]

# creating dict for lang -> ISO and ISO -> lang
zip_iterator_langToIso = zip(name_phoeble, iso_phoeble)
langToIso = dict(zip_iterator_langToIso)

zip_iterator_isoToLang = zip(iso_phoeble, name_phoeble)
isoToLang = dict(zip_iterator_isoToLang)

languages = list(set(languages_walsISO).intersection(iso_phoeble))

new_languages_walscodes = []
for code in languages_walscodes:
    if code in walsToISO:
        if walsToISO[code] not in languages:
            new_languages_walscodes.append(code)

wals_languages = []
for lang in new_languages_walscodes:
    wals_languages.append(wals[lang]["language"])

arr = list(set(wals_languages).intersection(name_phoeble))
arr_iso = [langToIso[elem] for elem in arr]
languages = languages + arr_iso


# # construction du nodes_lang.csv pour Neo4J

graphe_neo4j = open("../data/nodes_lang.csv","w")
graphe_neo4j.write("Languages, ISO 639-3, Genus, Family, Latitude, Longitude\n")

for i in range(len(languages)):
    strLangue = isoToLang[languages[i]]
    codeWals = ISOToWals[languages[i]]
    graphe_neo4j.write("\n" + strLangue+", "+languages[i]+", "+ wals[codeWals]["genus"]+", "+ wals[codeWals]["family"]+", "+ str(wals[codeWals]["latitude"])+", "+ str(wals[codeWals]["longitude"]))
graphe_neo4j.close()

