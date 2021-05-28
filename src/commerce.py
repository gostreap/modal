#%%
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from countryinfo import CountryInfo

from wals import dist

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
import operator


def create_commerce_data():
    imp = pd.read_csv("../data/HISTO_PAYS_IMPORT.csv")
    exp = pd.read_csv("../data/HISTO_PAYS_EXPORT.csv")
    pays = set(imp["Pays"]).intersection(exp["Pays"])

    data = dict()
    for p in pays:
        row_imp = imp.loc[imp["Pays"] == p]
        if len(row_imp) != 0:
            id = row_imp["Pays"].values[0]
            label = row_imp["Libellé"].values[0]
            import_value = int(row_imp["Année 2019"].values[0])
            export_value = int(exp.loc[exp["Pays"] == p]["Année 2019"].values[0])
            total_value = import_value + export_value
            data[id] = dict()
            data[id]["label"] = label
            data[id]["import"] = import_value
            data[id]["export"] = export_value
            data[id]["total"] = total_value

    sorted_data = dict(sorted(data.items(), key=operator.itemgetter(0)))
    json.dump(sorted_data, open("../data/commerce_exterieur.json", "w"))


def get_top_50():
    data = json.load(open("../data/commerce_exterieur.json", "r"))
    data.pop("QU")
    return dict(
        list(sorted(data.items(), key=lambda x: x[1]["total"], reverse=True))[:50]
    )


def get_country_code():
    code = dict()
    for line in open("../data/country_code", "r").readlines():
        a, b = line.split(" ")
        code[a] = b
    return code


def get_country_english(data):
    country_english = dict()
    gdp = pd.read_csv("../data/gdp.csv")
    code = get_country_code()
    for key in data.keys():
        country_english[key] = gdp.loc[gdp["Country Code"] == code[key].strip()][
            "Country Name"
        ].values[0]
    return country_english


def geo_dist(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).km


def add_geo_loc(data):
    app = Nominatim(user_agent="modal")
    country_english = get_country_english(data)
    for key in data.keys():
        print(CountryInfo(country_english[key]).capital())
        raw = app.geocode(
            "{}, {}".format(
                CountryInfo(country_english[key]).capital(), country_english[key]
            )
        ).raw
        data[key]["lat"] = raw["lat"]
        data[key]["lon"] = raw["lon"]


def add_gdp(data):
    gdp = pd.read_csv("../data/gdp.csv")
    code = get_country_code()
    years = [2019, 2018, 2017, 2016, 2015]
    for key in data.keys():
        row = gdp.loc[gdp["Country Code"] == code[key].strip()]
        for y in years:
            if not row[str(y)].isnull().values.any():
                data[key]["gdp"] = float(str(row[str(y)].values[0]).replace(",", "."))
                break


def add_dist_to_paris(data):
    paris_lat, paris_long = 48.8566969, 2.3514616

    for _, country in data.items():
        country["dist_to_paris"] = geo_dist(
            paris_lat, paris_long, country["lat"], country["lon"]
        )


def get_languages(data):
    lang = dict()
    app = Nominatim(user_agent="modal")
    country_english = get_country_english(data)
    for key in data.keys():
        lang[key] = CountryInfo(country_english[key]).languages()
    return lang


def set_country_lang(data):
    iso2 = get_languages(data)
    iso2to3 = dict()
    for key in iso2:
        for lang in iso2[key]:
            if lang not in iso2to3:
                s = input("Quel est le code iso3 de {} ? -> ".format(lang))
                iso2to3[lang] = s
    json.dump(iso2to3, open("../data/languages_iso2_to_iso3.json", "w"))


def get_iso2_to_iso3():
    return json.load(open("../data/languages_iso2_to_iso3.json", "r"))


def get_iso3_to_wals():
    return json.load(open("../data/iso3_to_wals.json", "r"))


def set_country_wals(data):
    iso2_to_iso3 = get_iso2_to_iso3()
    iso3_to_wals = get_iso3_to_wals()
    lang = get_languages(data)
    for key, l in lang.items():
        for i in range(len(l)):
            lang[key][i] = iso3_to_wals[iso2_to_iso3[l[i]]]
    json.dump(lang, open("../data/country_lang.json", "w"))


def get_country_wals():
    return json.load(open("../data/country_lang.json", "r"))


def add_dist_to_french(data):
    country_wals = get_country_wals()
    for country in data.keys():
        data[country]["dist_to_french"] = sum(
            [dist("fre", lang) for lang in country_wals[country]]
        ) / len([dist("fre", lang) for lang in country_wals[country]])


def set_country_final_data():
    data = dict(sorted(get_top_50().items(), key=operator.itemgetter(0)))
    add_gdp(data)
    add_geo_loc(data)
    add_dist_to_paris(data)
    add_dist_to_french(data)

    json.dump(data, open("../data/country_50.json", "w"))


def get_country_final_data():
    return json.load(open("../data/country_50.json", "r"))


#%%
set_country_final_data()


def simple_regr():
    data = get_country_final_data()
    X = []
    for key, country in data.items():
        if key != "MY":
            X.append(
                [
                    country["total"],
                    country["gdp"],
                    country["dist_to_paris"],
                    country["dist_to_french"],
                ]
            )
    print(
        pd.DataFrame(
            X, columns=["total", "gdp", "dist_to_paris", "dist_to_french"]
        ).corr()
    )

    X = []
    Y = []
    for key, country in data.items():
        if key != "MY":
            X.append(country["dist_to_french"])
            Y.append(country["total"])
    plt.plot(X, Y, "x")
    plt.show()


simple_regr
# %%
def final_data_to_gephi():
    data = get_country_final_data()
    nodes = open("../data/commerce_nodes.csv", "w")
    nodes.write("Id,Label, lat, lng, gdp, dist_to_french\n")
    nodes.write("FR,France,48.8566969,2.3514616,1778456492418,0\n")
    for key, country in data.items():
        if key == "MY":
            continue
        nodes.write(
            "{}, {}, {}, {}, {}, {}\n".format(
                key,
                country["label"],
                country["lat"],
                country["lon"],
                country["gdp"],
                country["dist_to_french"],
            )
        )
    nodes.close()

    edges = open("../data/commerce_edges.csv", "w")
    edges.write("Source,Target,Id,Weight,Type\n")
    for key, country in data.items():
        if key == "MY":
            continue
        edges.write(
            "{}, {}, {}, {}, {}\n".format(
                "FR",
                key,
                "FR"+key,
                country["total"],
                "directed"
            )
        )
    edges.close()
# %%
