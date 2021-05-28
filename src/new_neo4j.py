import json
import pandas as pd

# open Wals.json
file_wals = open("../data/wals.json", )
wals = json.load(file_wals)

# open phoible.csv
df_phoible = pd.read_csv(r"../data/phoeble.csv", low_memory = False)

wals_name = []
for _, lang in wals.items():
    wals_name.append(str.lower(lang["language"]))
wals_name = set(wals_name)
phoible_name = set(map(str.lower, df_phoible["LanguageName"]))

print(len(wals_name.intersection(phoible_name)))
languages = list(wals_name.intersection(phoible_name))
languages.sort()
print(languages)