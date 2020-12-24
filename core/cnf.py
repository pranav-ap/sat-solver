from .sentence import Iff, Implies, Negate, Symbol,  Unary, Binary, And, Or, arguments, expr


def to_cnf(s):
    s = eliminate_implications(s)
    s = move_not_inwards(s)
    s = distribute_and_over_or(s)
    return s


def eliminate_implications(s):
    if not isinstance(s, Iff) or not isinstance(s, Implies):
        return s

    left = eliminate_implications(s.left)
    right = eliminate_implications(s.right)

    if s.op == '=>':
        return right | ~left
    elif s.op == '<=>':
        return (left | ~right) & (right | ~left)


def move_not_inwards(s):
    """
    >>> move_not_inwards(~(A | B))
    (~A & ~B)
    """
    if isinstance(s, Symbol):
        return s

    elif isinstance(s, Binary):
        left = move_not_inwards(s.left)
        right = move_not_inwards(s.right)
        return expr(s.op, left, right)

    elif isinstance(s, Negate):
        # double negation

        if isinstance(s.operand, Negate):
            return move_not_inwards(s.operand.operand)

        # de morgans rule

        if isinstance(s.operand, Binary):
            left = move_not_inwards(~s.operand.left)
            right = move_not_inwards(~s.operand.right)

            if isinstance(s.operand, And):
                return associate('|', [left, right])
            elif isinstance(s.operand, Or):
                return associate('&', [left, right])

        return s


def first(iterable, default=None):
    """Return the first element of an iterable; or default."""
    return next(iter(iterable), default)


def distribute_and_over_or(s):
    """
    >>> distribute_and_over_or((A & B) | C)
    ((A | C) & (B | C))
    """
    if isinstance(s, Or):
        s = associate('|', arguments(s))

        if not isinstance(s, Or):
            return distribute_and_over_or(s)

        conj = first(arg for arg in arguments(s) if isinstance(arg, And))

        if not conj:
            return s

        others = [a for a in arguments(s) if a is not conj]
        rest = associate('|', others)
        return associate('&', [distribute_and_over_or(c | rest) for c in arguments(conj)])

    elif isinstance(s, And):
        left = distribute_and_over_or(s.left)
        right = distribute_and_over_or(s.right)
        return left & right

    return s


def combine(op, args):
    while True:
        if len(args) == 1:
            return args[0]
        elif len(args) == 2:
            return expr(op, *args)

        a, b, args = args[0], args[1], args[2:]
        c = expr(op, a, b)
        args.insert(0, c)


def associate(op, args):
    """
    >>> associate('&', [(A&B),(B|C),(B&C)])
    (A & B & (B | C) & B & C)
    """
    args = dissociate(op, args)

    if len(args) == 0:
        if op == '&':
            return True
        elif op == '|':
            return False

        return None

    elif len(args) == 1:
        return args[0]
    elif len(args) == 2:
        return expr(op, *args)

    return combine(op, args)


def dissociate(op, args):
    """
    >>> dissociate('&', [A & B])
    [A, B]
    """
    result = []

    def collect(subargs):
        for arg in subargs:
            if (isinstance(arg, Unary) or isinstance(arg, Binary)) and arg.op == op:
                collect(arguments(arg))
            else:
                result.append(arg)

    collect(args)
    return result


def conjuncts(s):
    """
    >>> conjuncts(A & B)
    [A, B]
    """
    return dissociate('&', [s])


def disjuncts(s):
    """
    >>> disjuncts(A | B)
    [A, B]
    """
    return dissociate('|', [s])
