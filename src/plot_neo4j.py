# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# %%
def plot_phoneme_inventory_size():
    data = pd.read_csv("../data/neo4j/phoneme_inventory_size_by_dataset.csv")
    set_dataset = set(data["ds"])
    grouped = data.groupby(data.ds)
    for s in set_dataset:
        histDataset = grouped.get_group(s)
        plt.hist(histDataset["AVG(c)"], bins=range(int(min(histDataset["AVG(c)"])), int((max(histDataset["AVG(c)"])))+1))
    plt.show()

plot_phoneme_inventory_size()

# %%


