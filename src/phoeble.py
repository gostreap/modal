# %%
import pandas as pd
from lingtypology.datasets import Phoible


# %%
def write_data():
    data = Phoible(aggregated=False).get_df()
    data.to_csv("../data/phoeble.csv", index=False)


# %%
def load_data():
    return pd.read_csv("../data/phoeble.csv", low_memory=False)


# %%
def get_iso(data, iso):
    return data[data["ISO6393"] == iso]


# %%
def get_phoneme(data, phoneme):
    return data[data["Phoneme"] == phoneme]


# %%
# Exemple : return all phoneme "b" in French
data = load_data()
print(get_phoneme(get_iso(data, "fra"), "b"))
# %%
