from core.cnf import to_cnf
from core import KnowledgeBase, make_symbols, true, false


def main():
    P11, P12, P21, P22, P31, B11, B21 = make_symbols(
        'P11 P12 P21 P22 P31 B11 B21')

    kb = KnowledgeBase()

    kb.tell(~P11)
    kb.tell(B11 % (P12 | P21))
    kb.tell(B21 % (P11 | P22 | P31))
    kb.tell(~B11)
    kb.tell(B21)

    result = kb.ask_if_true(P22)
    print(result)


if __name__ == '__main__':
    main()
