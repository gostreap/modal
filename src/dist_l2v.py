import lang2vec.lang2vec as l2v

dist = l2v.distance('syntactic', list(l2v.LANGUAGES))

print(dist)