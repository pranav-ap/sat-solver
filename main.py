from core.tt_entails import tt_entails
from core import KnowledgeBase, make_symbols, to_cnf, true, false


def main():
    (A, B, C, D, E) = make_symbols('A B C D E')

    kb = KnowledgeBase()

    kb.tell(~(B | C))
    kb.tell((A & B) | C)
    kb.tell(A & (B | (D & E)))

    x = kb.get_all_clauses()
    print(x)


if __name__ == '__main__':
    main()
