from core import *
import pytest


def test_basic_tt_entails():
    P, Q = make_symbols('P Q')
    result = tt_entails(P & Q, P)
    assert result == True
