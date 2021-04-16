import lang2vec.lang2vec as l2v

dist = l2v.distance('syntactic', list(l2v.LANGUAGES))

# creating graphe_1.txt
graphe_1 = open("Graphe_1.txt","a")
graphe_1. truncate(0)
graphe_1.write("Source,Target,Id,Length\n")
for i in range(len(dist)):
    #string = str(streets[i][0])+","+str(streets[i][1])+","+str(streets[i][2])+","+str(1/streets[i][3])
    graphe_1.write(string+"\n")
graphe_1.close()