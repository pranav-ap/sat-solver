from .cnf import associate, conjuncts, disjuncts, to_cnf
from .sentence import And, Binary, Iff, Implies, Negate, Or, Symbol, Unary, arguments
from .utils import extend, unique, remove_all, append_unique
from collections import defaultdict


def prop_symbols(x):
    if isinstance(x, Symbol):
        return {x}

    return {symbol for arg in arguments(x) for symbol in prop_symbols(arg)}


def pl_true(exp, model):
    """
    Check if the propositional logic expression is true in the model
    """
    if isinstance(exp, Symbol):
        if exp.operand in (True, False):
            return exp.operand

        return model.get(exp)

    if isinstance(exp, Unary):
        operand = exp.operand

        if isinstance(exp, Negate):
            p = pl_true(operand, model)

            if p is None:
                return None
            else:
                return not p

    elif isinstance(exp, Binary):
        args = [exp.left, exp.right]

        if isinstance(exp, And):
            result = True

            for arg in args:
                p = pl_true(arg, model)

                if p is False:
                    return False
                elif p is None:
                    result = None

            return result

        elif isinstance(exp, Or):
            result = False

            for arg in args:
                p = pl_true(arg, model)

                if p is True:
                    return True
                elif p is None:
                    result = None

            return result

        elif isinstance(exp, Implies):
            p, q = args
            return pl_true(~p | q, model)

        elif isinstance(exp, Iff):
            p, q = args

            pt = pl_true(p, model)

            if pt is None:
                return None

            qt = pl_true(q, model)

            if qt is None:
                return None

            return pt == qt

        else:
            raise ValueError('Illegal operator in logic expression' + str(exp))


# TT Entails


def tt_check_all(kb, alpha, symbols, model):
    if not symbols:
        if pl_true(kb, model):
            result = pl_true(alpha, model)
            assert result is not None
            return result
        else:
            return True
    else:
        P, rest = symbols[0], symbols[1:]
        return (tt_check_all(kb, alpha, rest, extend(model, P, True)) and
                tt_check_all(kb, alpha, rest, extend(model, P, False)))


def tt_entails(kb, alpha):
    """
    >>> tt_entails(expr('P & Q'), expr('Q'))
    True
    """
    symbols = list(prop_symbols(kb & alpha))
    return tt_check_all(kb, alpha, symbols, {})


#  PL Resolution

def pl_resolve(ci, cj):
    clauses = []

    ci_disjuncts = disjuncts(ci)
    cj_disjuncts = disjuncts(cj)

    for di in ci_disjuncts:
        di = to_cnf(di)

        for dj in cj_disjuncts:
            dj = to_cnf(dj)

            if di == ~dj or ~di == dj:
                x = unique(remove_all(di, ci_disjuncts) +
                           remove_all(dj, cj_disjuncts))
                y = associate('|', x)
                clauses.append(y)

    return clauses


def pl_resolution(clauses, alpha):
    """
    >>> pl_resolution(horn_clauses_KB, A)
    True
    """
    clauses = list(clauses) + conjuncts(to_cnf(~alpha))
    new = set()

    while True:
        n = len(clauses)
        pairs = [(clauses[i], clauses[j])
                 for i in range(n)
                 for j in range(i + 1, n)]

        for (ci, cj) in pairs:
            resolvents = pl_resolve(ci, cj)

            if False in resolvents:
                return True

            new.update(resolvents)

        if new.issubset(set(clauses)):
            return False

        append_unique(clauses, new)


# chaining


def is_definite_clause(s):
    """
    A definite clause looks like this:
    A & B & ... & C ==> D
    """
    if isinstance(s, Symbol):
        return True
    elif isinstance(s, Implies):
        antecedent, consequent = s.left, s.right
        return isinstance(consequent, Symbol) and all(isinstance(arg, Symbol) for arg in conjuncts(antecedent))

    return False


def parse_definite_clause(s):
    assert is_definite_clause(s)

    if isinstance(s, Symbol):
        return [], s

    antecedent, consequent = s.left, s.right
    return conjuncts(antecedent), consequent


def pl_forward_chaining_entails(kb, query):
    """
    >>> pl_fc_entails(horn_clauses_KB, expr('Q'))
    True
    """
    count = {c: len(conjuncts(c.left))
             for c in list(kb.clauses) if isinstance(c, Implies)}

    inferred = defaultdict(bool)
    agenda = [s for s in list(kb.clauses) if isinstance(s, Symbol)]

    while agenda:
        premise_symbol = agenda.pop()

        if premise_symbol == query:
            return True

        if not inferred[premise_symbol]:
            inferred[premise_symbol] = True

            for clause in kb.clauses_with_premise(premise_symbol):
                count[clause] -= 1

                if count[clause] == 0:
                    agenda.append(clause.right)

    return False
