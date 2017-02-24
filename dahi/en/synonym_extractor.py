from nltk.corpus import wordnet
from itertools import chain


class EnglishSynoymer(object):
    """docstring for EnglishSynoymer"""
    def __init__(self):
        super(EnglishSynoymer, self).__init__()
        self.unnecessary_stop_words = ["be", "are", "is", "do", "can"]

    def findSynonyms(self, word ,tag):
        synonyms = wordnet.synsets(word, tag)
        lemmas = set(chain.from_iterable([word.lemma_names() for word in synonyms]))
        lemmas = [i.lower() for i in lemmas if i.lower() not in self.unnecessary_stop_words]
        return lemmas
