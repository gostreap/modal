# # import nltk
# # nltk.download()

# from nltk.corpus import words
# word_list = words.words()
# # prints 236736
# print(len(word_list))

# print(word_list[:20])

import lang2vec.lang2vec as l2v
print(l2v.DISTANCES)
# print(l2v.LANGUAGES)

l2v.distance('syntactic', 'fra', 'eng')