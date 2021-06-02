# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# %%
def plot_phoneme_inventory_size():
    data = pd.read_csv("../data/neo4j_results/phoneme_inventory_size_by_dataset.csv")
    set_dataset = set(data["ds"])
    grouped = data.groupby(data.ds)
    for s in set_dataset:
        histDataset = grouped.get_group(s)
        plt.hist(histDataset["AVG(c)"], bins=range(int(min(histDataset["AVG(c)"])), int((max(histDataset["AVG(c)"])))+1),label=s, rwidth=0.5)
    plt.xlabel("Phoneme Inventory Size", fontsize=12)
    plt.ylabel("Number of Languages", fontsize=12)
    plt.legend(title="Dataset")
    plt.show()

# plot_phoneme_inventory_size()

# %%
def count_couple():
    data = pd.read_csv("../data/neo4j_results/consonant_vowel_by_dialect.csv")
    dic_cons = dict()
    for idx, row in data.iterrows():
        if row["Consonant"] not in dic_cons:
            dic_cons[row["Consonant"]] = dict()
            dic_cons[row["Consonant"]][row["Vowel"]] = 1
        else:
            if row["Vowel"] not in dic_cons[row["Consonant"]]:
                dic_cons[row["Consonant"]][row["Vowel"]] = 1
            else:
                dic_cons[row["Consonant"]][row["Vowel"]] += 1
    for i, row in data.iterrows():
        data.at[i, 'Group'] = dic_cons[row["Consonant"]][row["Vowel"]]
    return data



def plot_vowel_consonant():
    data = count_couple()
    sns.set(rc={"figure.figsize": (24, 10)})
    sns.scatterplot(data=data, x=data["Consonant"], y=data["Vowel"], hue=data["Group"])
    plt.show()


plot_vowel_consonant()
# %%
