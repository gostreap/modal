# from google_trans_new import google_translator
from googletrans import Translator

english_words = []
# opening the text file
with open("../data/google-10000-english.txt", "r") as file:
    # reading each line
    for line in file:
        english_words.append(line.strip())


# def english_to_lang(lang, words):
#     dictionary = dict()
#     translator = Translator()
#     for word in words:
#         rep = translator.translate(word, lang_src="en", lang_tgt=lang, pronounce=True)
#         dictionary[word] = [
#             rep[0] if type(rep) == str else rep[0][0],
#             rep[2]
#             if rep[2] is not None
#             else (rep[0] if type(rep) == str else rep[0][0]),
#         ]
#         # print(rep)
#     return dictionary




# d = english_to_lang("fr", english_words[:100])
# print(d)

translator = Translator()
res = translator.translate(english_words[:100], src="en", dest="fr")
for trad in res:
    print(trad)
