# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# %%
def plot_phoneme_inventory_size():
    data = pd.read_csv("../data/neo4j/phoneme_inventory_size_by_dataset.csv")
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
def plot_vowel_consonant():
    data = pd.read_csv("../data/neo4j/consonant_vowel_by_dialect.csv")
    sns.set(rc={"figure.figsize": (15, 25)})
    sns.scatterplot(data=data, x=data["Consonant"], y=data["Vowel"])
    plt.show()


plot_vowel_consonant()