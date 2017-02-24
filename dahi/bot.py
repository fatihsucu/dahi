from dahi.document import Document
from dahi.matchers.tfidfMatcher import TFIDFMatcher
from dahi.nlu import NLU, MatchNotFound
from dahi.statement import Statement
from dahi.postagger import EnglishPosTagger
from dahi.lemmatizer import EnglishLemmatizer

class Bot(object):

    def __init__(self, knowledgeBase):
        self.knowledgeBase = knowledgeBase
        self.matcher = TFIDFMatcher(knowledgeBase)
        self.nlu = NLU(self.matcher, self.knowledgeBase, EnglishPosTagger(), EnglishLemmatizer())
        
    def respond(self, statement):
        count = self.knowledgeBase.count()
        threshold = 0.5 + 0.0002 * float(count)
        # try:
        docID, score = self.nlu.findAnswer(
            statement.text, threshold=threshold, amount=4)
        print("Match Score : {}".format(score))
        doc = self.knowledgeBase.get(docID)
        if doc.botSay:
            statement = doc.botSay
        # except MatchNotFound as e:
        #     FIXME: this should not be literal, instead, knowledgeBase can be
        #     used to get this.
            # statement = Statement("sorry, I did not get it.")
        return doc

    def learn(self, doc):
        self.nlu.insertKnowledbase(doc)
        self.matcher.refresh()
