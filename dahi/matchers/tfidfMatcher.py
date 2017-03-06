import math

import operator

from dahi.matchers.abstracts import AbstractMatcher
from dahi.nlu import tokenize
from dahi.matchers.model import Model
from copy import deepcopy


class TFIDFMatcher(AbstractMatcher):

    def __init__(self, knowledgeBase):
        super(TFIDFMatcher, self).__init__()
        self.knowledgeBase = knowledgeBase
        self.model = self.generateModel(knowledgeBase)

    @classmethod
    def generateModel(cls, knowledgeBase):
        """
        returns a new TF-IDF model populated with the given knowledgeBase.

        :param knowledgeBase: KnowledgeBase instance
        :return: Model instance
        """
        model = Model()
        # filling the table with tf values for each term found in docs
        for doc in knowledgeBase.getAll():
            if not doc.entities:
                continue
            entities = doc.entities

            if not entities:
                entities = []
                for i in doc.humanSay.text.split(" "):
                    entities.append({"lemma": i, "tag": "NN"})

            n = len(entities)
            for entity in entities:
                tf = model.getTF(docId=doc.id, term=entity["lemma"])
                tf = float(tf * n + 1) / n
                model.setTF(
                    docId=doc.id, term=entity["lemma"], tag=entity["tag"][0].lower(), frequency=tf)

        # filling the model with idf values for each term found in the model
        for term in model.getTerms():
            df = model.getDF(term)
            idf = math.log(knowledgeBase.count() / float(1 + df))
            if idf <= 0:
                idf = 1
            model.setIDF(term, idf)

        return model

    def getTfIdfScore(self, term, docId):
        """
        returns the TF-IDF score according to term and docId

        :param term:
        :param docId:
        :return:
        """
        tf = self.model.getTF(docId, term)
        if not tf:
            return None
        return tf * float(self.model.getIDF(term))

    def match(self, text, length=5):
        """
        matches given text against the knowledge base.

        the best matching knowledge base documents will be returned in a list.
        This list will be sorted descending by matching score.

        :param text: query text
        :param length: length of matching list to be returned
        :return: list of the best matching knowledge base documents
        """
        docScores = {}

        for term in tokenize(text):
            for docId in self.model.getDocIds(term):
                termScore = self.model.getScore(docId, term)
                docScores[docId] = docScores.get(docId, 0) + termScore

        return sorted(
            docScores.items(),
            key=operator.itemgetter(1),
            reverse=True)[:length]

    def refresh(self):
        self.model = self.generateModel(self.knowledgeBase)

    def getSynonyms(self):
        return self.model.synonyms.keys()

    def getMainTermOf(self, term):
        return self.model.synonyms[term]

