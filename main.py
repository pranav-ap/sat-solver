from core.knowledge_base import PropDefiniteKB
from core.cnf import to_cnf
from core import KnowledgeBase, make_symbols, true, false


def main():
    (A, B, C, D, E, F, G, H, I, J) = make_symbols('A B C D E F G H I J')

    clauses = [(B & F) >> E,
               (A & E & F) >> G,
               (B & C) >> F,
               (A & B) >> D,
               (E & F) >> H,
               (H & I) >> J,
               A,
               B,
               C]

    kb = PropDefiniteKB()

    for clause in clauses:
        kb.tell(clause)

    result = kb.ask_if_true(G)
    print(result)


if __name__ == '__main__':
    main()
