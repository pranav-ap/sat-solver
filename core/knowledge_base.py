class KnowledgeBase():
    def __init__(self):
        self.sentences = set()
        self.trees = set()

    def size(self):
        return len(self.sentences)

    def tell(self, sentence):
        self.sentences.add(sentence)

    def remove(self, sentence):
        self.sentences.remove(sentence)

    def as_sentence(self):
        single_sentence = ' ) and ( '.join(self.sentences)
        single_sentence = '( ' + single_sentence + ' )'
        return single_sentence
