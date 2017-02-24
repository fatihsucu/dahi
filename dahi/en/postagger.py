from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
import nltk


class EnglishPosTagger(object):
    """docstring for PosTagger"""
    def __init__(self):
        super(EnglishPosTagger, self).__init__()
        self.posTagger = nltk
        

    def tag(self, tokinezed_sentence):
        tagged_sentence = self.posTagger.pos_tag(tokinezed_sentence)
        return tagged_sentence

    def filterTags(self, tagged_sentence):
        filtered = ""
        for word, tag in tagged_sentence:
            if tag.startswith("N"):
                filtered += "{} ".format(word)
            if tag.startswith("V") and tag != "VBZ" and tag != "VBP":
                filtered += "{} ".format(word)
        return filtered

    def filterTagsViaValues(self, tagged_sentence):
        filtered = []
        for word, tag in tagged_sentence:
            if tag.startswith("N"):
                filtered.append((word, tag))
            if tag.startswith("V") and tag != "VBZ" and tag != "VBP":
                filtered.append((word, tag))
        return filtered

    def getSpesificWords(self, sentence):
        tokinezed = word_tokenize(sentence)
        tagged = self.filterTags(tokinezed)
        return self.filterTags(tagged)

    def getSpesificWordsWithTags(self, sentence):
        tokinezed = word_tokenize(sentence)
        tagged = self.tag(tokinezed)
        result = {}
        for word, tag in self.filterTagsViaValues(tagged):
            result[word] = tag
        return result





