class DefaultLanguage(object):

    def __init__(self):
        pass

    def analyze(self, text):
        return text


class MatchNotFound(Exception):
    def __init__(self, message="no answer matched", code=400):
        super(MatchNotFound, self).__init__(message)
        self.message = message
        self.code = code

    def __json__(self):
        return {
            "type": self.__class__.__name__,
            "message": self.message,
            "code": self.code}

    def __str__(self):
        return "{}: code: {}, message: {}".format(
            self.__class__.__name__,
            self.code,
            self.message)


class NLU(object):

    def __init__(self, matcher, knowledgebase, lang='en'):
        super(NLU, self).__init__()
        self.knowledgebase = knowledgebase
        self.matcher = matcher
        self.source = __import__('dahi')
        try:
            self.language = self.source.__getattribute__(lang)
        except Exception as e:
            self.language = DefaultLanguage()

    def findBestMatch(self, matches):
        bestMatch = matches[0]
        score = bestMatch[1]
        if score > 0.5:
            return bestMatch

    def findTermFromSynonym(self, text):
        synonyms = self.matcher.getSynonyms()
        for key in text.split(" "):
            if key in synonyms:
                text = text.replace(key, self.matcher.getMainTermOf(key))
        return text

    def findAnswer(self, text, **kwargs):
        text = text.lower()
        text = self.findTermFromSynonym(text)
        lemma_list = self.language.analyze(text)
        matches = self.matcher.match(" ".join([t["lemma"] for t in lemma_list]))
        if not matches:
            raise MatchNotFound()

        bestMatch = self.findBestMatch(matches)
        if not bestMatch:
            raise MatchNotFound()

        docID = bestMatch[0]
        score = bestMatch[1]
        return docID, score

    def insertKnowledbase(self, doc):
        text = doc.humanSay.text
        text = text.lower()
        lemma_list = self.language.analyze(text)
        doc.setEntities(lemma_list)
        self.knowledgebase.insert(doc)


def tokenize(text):
    return [t for t in text.split(" ")]

#
# def tf(term, document):
#     terms = tokenize(document)
#     term_frequency = terms.count(term)
#     document_size = len(terms)
#     return float(term_frequency) / document_size
#
#
# def countDocsContains(term, docs):
#     return sum(1 for i in docs if term in i)
#
#
# def idf(term, docs):
#     return math.log(len(docs) / (float(countDocsContains(term, docs))))
#
#
# def sigmoid(x):
#     return 1 / (1 + math.exp(-x))

