from core import *
import pytest


def test_simple_tt_entails():
    P, Q = make_symbols('P Q')
    result = tt_entails(P & Q, P)
    assert result == True


def test_cnf_convert():
    (A, B, C, D, E) = make_symbols('A B C D E')

    kb = KnowledgeBase()

    kb.tell(~(B | C))
    kb.tell((A & B) | C)
    kb.tell(A & (B | (D & E)))
    kb.tell(A & B | D & E)

    x = kb.get_all_clauses()

    assert len(x) > 0
