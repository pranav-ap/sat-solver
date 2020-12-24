from .cnf import associate, conjuncts, disjuncts, to_cnf
from .sentence import And, Binary, Iff, Implies, Negate, Or, Symbol, Unary, arguments


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


def extend(s, var, val):
    return {**s, var: val}

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

def append_unique(clauses, new):
    for c in new:
        if c not in clauses:
            clauses.append(c)


def unique(seq):
    return list(set(seq))


def remove_all(item, seq):
    if isinstance(seq, str):
        return seq.replace(item, '')
    elif isinstance(seq, set):
        rest = seq.copy()
        rest.remove(item)
        return rest
    else:
        return [x for x in seq if x != item]


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

            if len(resolvents) > 0:
                resolvents = resolvents

            if False in resolvents:
                return True

            new.update(resolvents)

        if new.issubset(set(clauses)):
            return False

        append_unique(clauses, new)
