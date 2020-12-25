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


def test_wumpus_world():
    P11, P12, P21, P22, P31, B11, B21 = make_symbols(
        'P11 P12 P21 P22 P31 B11 B21')

    kb = KnowledgeBase()

    kb.tell(~P11)
    kb.tell(B11 % (P12 | P21))
    kb.tell(B21 % (P11 | P22 | P31))
    kb.tell(~B11)
    kb.tell(B21)

    result = kb.ask_if_true(P22)
    assert result
