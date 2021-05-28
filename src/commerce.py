from geopy.geocoders import Nominatim
from countryinfo import CountryInfo

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


def get_country_english(data):
    country_english = dict()
    gdp = pd.read_csv("../data/gdp.csv")
    code = get_country_code()
    for key in data.keys():
        country_english[key] = gdp.loc[gdp["Country Code"] == code[key].strip()][
            "Country Name"
        ].values[0]
    return country_english


def get_geo_loc(data):
    app = Nominatim(user_agent="modal")
    country_english = get_country_english(data)
    for key in data.keys():
        print(CountryInfo(country_english[key]).capital())
        print(
            app.geocode(
                "{}, {}".format(
                    CountryInfo(country_english[key]).capital(), country_english[key]
                )
            ).raw
        )


def get_languages(data):
    app = Nominatim(user_agent="modal")
    country_english = get_country_english(data)
    for key in data.keys():
        print(country_english[key], CountryInfo(country_english[key]).languages())


data = get_top_50()
sorted_data = dict(sorted(data.items(), key=operator.itemgetter(0)))

add_gdp(sorted_data)

# c = 1
# for key, q in sorted_data.items():
#     print(c, key, q)
#     c += 1


get_languages(data)
print(CountryInfo("Lebanon").languages())