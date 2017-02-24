from dahi.en.lemmatizer import EnglishLemmatizer
from dahi.en.postagger import EnglishPosTagger


def analyze(text):
    entities = EnglishPosTagger().getSpesificWordsWithTags(text)
    lemma_dictionary = EnglishLemmatizer().lemmatizeViaTag(entities)
    return lemma_dictionary