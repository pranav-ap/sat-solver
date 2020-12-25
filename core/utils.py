def first(iterable, default=None):
    return next(iter(iterable), default)


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


def extend(s, var, val):
    return {**s, var: val}
