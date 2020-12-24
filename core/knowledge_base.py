from .cnf import associate, conjuncts, to_cnf
from .prop_logic import pl_resolution, tt_entails


class KnowledgeBase:
    def __init__(self):
        self.clauses = set()

    def tell(self, sentence):
        clauses = conjuncts(to_cnf(sentence))
        self.clauses.update(clauses)

    def ask_if_true(self, query):
        # sentence = self.get_as_sentence()
        # return tt_entails(sentence, query)
        return pl_resolution(self.clauses, query)

    # utils

    def get_as_sentence(self):
        if len(self.clauses) == 0:
            return None
        elif len(self.clauses) == 1:
            return self.clauses[0]

        return associate('&', self.clauses)

    def size(self):
        return len(self.clauses)
