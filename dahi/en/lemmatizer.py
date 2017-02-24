import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

def is_noun(tag):
    return tag in ['NN', 'NNS', 'NNP', 'NNPS']


def is_verb(tag):
    return tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']


def is_adverb(tag):
    return tag in ['RB', 'RBR', 'RBS']


def is_adjective(tag):
    return tag in ['JJ', 'JJR', 'JJS']


def penn_to_wordnet(tag):
    if is_adjective(tag):
        return wordnet.ADJ
    elif is_noun(tag):
        return wordnet.NOUN
    elif is_adverb(tag):
        return wordnet.ADV
    elif is_verb(tag):
        return wordnet.VERB
    return None


class EnglishLemmatizer(object):
    """docstring for Lemmatizer"""
    def __init__(self):
        super(EnglishLemmatizer, self).__init__()
        self.lemmatizer = nltk.stem.WordNetLemmatizer()

    def lemmatize(self, word, tag=None):
        if tag:
            return self.lemmatizer.lemmatize(word, tag)
        return self.lemmatizer.lemmatize(word)

    def lemmatizeViaTag(self, sentence_dictionary):
        """
        Sentence Dictionary should be:
        key: word
        value: tag
        """
        result = []
        for word, tag in sentence_dictionary.items():
            lemma = self.lemmatize(word, penn_to_wordnet(tag))
            result.append({"lemma" : lemma, "tag": tag})
        return result

