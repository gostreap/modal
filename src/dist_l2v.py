# %%
import lang2vec.lang2vec as l2v
import pandas as np

# %%
dist = l2v.distance('syntactic', list(l2v.LANGUAGES))

# %%
df = np.DataFrame(dist)
df.write_csv("../data/dist_l2v.csv")