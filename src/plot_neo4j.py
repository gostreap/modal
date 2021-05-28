# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# %%
def plot_phoneme_inventory_size():
    data = pd.read_csv("../data/neo4j/phoneme_inventory_size.csv")
    plt.hist(data["C"], bins=range(10, max(data["C"])))

plot_phoneme_inventory_size()
# %%
