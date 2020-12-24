from collections import defaultdict
from .cnf import associate, conjuncts, to_cnf
from .tt_entails import tt_entails


class KnowledgeBase:
    def __init__(self):
        self.clauses = defaultdict(set)  # sentence => { clauses }

    def tell(self, sentence):
        clauses = to_cnf(sentence)
        self.clauses[sentence].add(clauses)

    def get_as_sentence(self):
        clauses = self.get_all_clauses()

        if len(clauses) == 0:
            return None
        elif len(clauses) == 1:
            return clauses[0]

        return associate('&', clauses)

    def ask_if_true(self, query):
        sentence = self.get_as_sentence()
        return tt_entails(sentence, query)

    # utils

    def get_all_clauses(self):
        clauses = []

        for clauses_set in self.clauses.values():
            clauses.extend(clauses_set)

        return clauses

    def remove(self, sentence):
        self.clauses.pop(sentence)

    def size(self):
        return len(self.clauses)
