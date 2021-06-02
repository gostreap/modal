#import lang2vec.lang2vec as l2v
import pandas as np
import scipy

# Write distance matrix
# dist = l2v.distance('syntactic', list(l2v.LANGUAGES))
# df = np.DataFrame(dist)
# df.to_csv("../data/dist_l2v_syntactic.csv")

# Load distance matrix
df = np.read_csv("../data/common/dist_l2v_syntactic.csv")
dist = df.to_numpy()
dist = dist[:,1:]

# creating graphe_1.txt
epsilon = 0.00001
graphe_1 = open("Graphe_1.txt","a")
graphe_1. truncate(0)
graphe_1.write("Source,Target,Id,Length\n")

for i in range(len(dist)):
    for j in range(len(dist)):
        string = str(i)+","+str(i)+","+str(i*len(dist)+j)+","+str(1/(dist[i][j]+epsilon))
        graphe_1.write(string+"\n")
graphe_1.close()

