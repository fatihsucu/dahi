class Model(object):
    """
    Term-frequency and inverse-document-frequency data model. This facilitates
    storing and querying TF and IDF values.
    """

    """
    every individual term has the following entry in the data dictionary
    """
    TERM_ENTRY = {
        "tf": {},
        "idf": 0
    }

    def __init__(self):
        super(Model, self).__init__()
        self.data = {}

    def empty(self):
        self.data = {}

    def getEntry(self, term):
        """
        returns the term entry of the model.

        :param term: term as a string
        :return: TERM_ENTRY structured data
        """
        return self.data.get(term, deepcopy(Model.TERM_ENTRY))

    def setTF(self, docId, term, frequency):
        """
        sets the term-frequency value of the given document.

        :param docId: document id
        :param term: term as a string
        :param frequency: frequency as an integer value
        :return:
        """
        entry = self.getEntry(term)
        entry["tf"][docId] = frequency
        self.data[term] = entry

    def setIDF(self, term, frequency):
        """
        sets the inverse-document-frequency of the given term

        :param term: term as a string
        :param frequency: integer
        :return:
        """
        entry = self.getEntry(term)
        entry["idf"] = frequency
        self.data[term] = entry

    def getTF(self, docId, term):
        """
        returns the term-frequency of the given document.

        if either the term or docId does not exists in the model, this will
        return 0 (zero).

        :param docId: document id
        :param term: term as a string
        :return: frequency as an integer value
        """
        # @TODO: test with not available docId and term
        entry = self.getEntry(term)
        return entry["tf"].get(docId, 0)

    def getIDF(self, term):
        """
        returns the inverse-document-frequency of the given term.

        if term does not exists in the model, this will return 0.

        :param term: term as a string
        :return: integer
        """
        entry = self.getEntry(term)
        return entry["idf"]

    def getDF(self, term):
        """
        returns the document frequency of the given term.

        document frequency is the count of how many distinct documents the term
        occurs in.

        :param term:
        :return: document frequency as an integer value
        """
        return len(self.data[term]["tf"])

    def getTerms(self):
        """
        returns all the terms found in the model.

        :return: terms list
        """
        return self.data.keys()

    def getDocIds(self, term):
        """
        returns the list of document ids in which the given term exists

        :param term: term as a string
        :return: document ids list
        """
        entry = self.getEntry(term)
        return entry["tf"].keys()

    def getScore(self, docId, term):
        """
        calculates and returns TF-IDF score according to docId and term

        :param docId: document id
        :param term: term as a string
        :return: float
        """
        tf = self.getTF(docId, term)
        idf = self.getIDF(term)
        return tf * idf
