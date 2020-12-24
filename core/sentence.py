class Expression:
    pass


class Symbol(Expression):
    def __init__(self, operand):
        self.operand = operand

    # Operator overloads

    def __invert__(self):
        return Negate(self)

    def __and__(self, rhs):
        return And(self, rhs)

    def __or__(self, rhs):
        return Or(self, rhs)

    def __rshift__(self, rhs):
        return Implies(self, rhs)

    def __mod__(self, rhs):
        return Iff(self, rhs)

    # Reverse operator overloads

    def __rand__(self, lhs):
        return And(lhs, self)

    def __ror__(self, lhs):
        return Or(lhs, self)

    def __rrshift__(self, lhs):
        return Implies(lhs, self)

    def __mod__(self, lhs):
        return Iff(lhs, self)

    # repr

    def __str__(self):
        return str(self.operand)

    def __repr__(self):
        return str(self.operand)

    def __hash__(self):
        return hash(self.operand)

    def __eq__(self, other):
        return isinstance(other, Symbol) and self.operand == other.operand


true = Symbol(True)
false = Symbol(False)


class Unary(Expression):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

    # repr

    def __str__(self):
        return ' '.join([self.op, str(self.operand)])

    def __repr__(self):
        return ' '.join([self.op, str(self.operand)])

    def __hash__(self):
        return hash(' '.join([self.op, str(self.operand)]))

    def __eq__(self, other):
        return isinstance(other, Unary) and self.operand == other.operand and self.op == other.op


class Negate(Unary):
    def __init__(self, operand):
        super().__init__('~', operand)

    # Operator overloads

    def __invert__(self):
        return Negate(self)

    def __and__(self, rhs):
        return And(self, rhs)

    def __or__(self, rhs):
        return Or(self, rhs)

    def __rshift__(self, rhs):
        return Implies(self, rhs)

    def __mod__(self, rhs):
        return Iff(self, rhs)

    # Reverse operator overloads

    def __rand__(self, lhs):
        return And(lhs, self)

    def __ror__(self, lhs):
        return Or(lhs, self)

    def __rrshift__(self, lhs):
        return Implies(lhs, self)

    def __mod__(self, rhs):
        return Iff(self, rhs)


class Binary(Expression):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    # repr

    def __str__(self):
        return ' '.join([str(self.left), self.op, str(self.right)])

    def __repr__(self):
        return ' '.join([str(self.left), self.op, str(self.right)])

    def __hash__(self):
        return hash(' '.join([str(self.left), self.op, str(self.right)]))

    def __eq__(self, other):
        return isinstance(other, Binary) and self.left == other.left and self.right == other.right and self.op == other.op


class And(Binary):
    def __init__(self, left, right):
        super().__init__('&', left, right)

    # Operator overloads

    def __invert__(self):
        return Negate(self)

    def __and__(self, rhs):
        return And(self, rhs)

    def __or__(self, rhs):
        return Or(self, rhs)

    def __rshift__(self, rhs):
        return Implies(self, rhs)

    def __mod__(self, rhs):
        return Iff(self, rhs)

    # Reverse operator overloads

    def __rand__(self, lhs):
        return And(lhs, self)

    def __ror__(self, lhs):
        return Or(lhs, self)

    def __rrshift__(self, lhs):
        return Implies(lhs, self)

    def __mod__(self, lhs):
        return Iff(lhs, self)


class Or(Binary):
    def __init__(self, left, right):
        super().__init__('|', left, right)

    # Operator overloads

    def __invert__(self):
        return Negate(self)

    def __and__(self, rhs):
        return And(self, rhs)

    def __or__(self, rhs):
        return Or(self, rhs)

    def __rshift__(self, rhs):
        return Implies(self, rhs)

    def __mod__(self, rhs):
        return Iff(self, rhs)

    # Reverse operator overloads

    def __rand__(self, lhs):
        return And(lhs, self)

    def __ror__(self, lhs):
        return Or(lhs, self)

    def __rrshift__(self, lhs):
        return Implies(lhs, self)

    def __mod__(self, lhs):
        return Iff(lhs, self)


class Implies(Binary):
    def __init__(self, left, right):
        super().__init__('=>', left, right)

    # Operator overloads

    def __invert__(self):
        return Negate(self)

    def __and__(self, rhs):
        return And(self, rhs)

    def __or__(self, rhs):
        return Or(self, rhs)

    def __rshift__(self, rhs):
        return Implies(self, rhs)

    def __mod__(self, rhs):
        return Iff(self, rhs)

    # Reverse operator overloads

    def __rand__(self, lhs):
        return And(lhs, self)

    def __ror__(self, lhs):
        return Or(lhs, self)

    def __rrshift__(self, lhs):
        return Implies(lhs, self)

    def __mod__(self, lhs):
        return Iff(lhs, self)


class Iff(Binary):
    def __init__(self, left, right):
        super().__init__('<=>', left, right)

    # Operator overloads

    def __invert__(self):
        return Negate(self)

    def __and__(self, rhs):
        return And(self, rhs)

    def __or__(self, rhs):
        return Or(self, rhs)

    def __rshift__(self, rhs):
        return Implies(self, rhs)

    def __mod__(self, rhs):
        return Iff(self, rhs)

    # Reverse operator overloads

    def __rand__(self, lhs):
        return And(lhs, self)

    def __ror__(self, lhs):
        return Or(lhs, self)

    def __rrshift__(self, lhs):
        return Implies(lhs, self)

    def __mod__(self, lhs):
        return Iff(lhs, self)


# Utils


def make_symbols(symbols):
    return [Symbol(symbol) for symbol in symbols.split()]


def expr(op, *args):
    if op == '~':
        return Negate(*args)
    elif op == '&':
        return And(*args)
    elif op == '|':
        return Or(*args)
    elif op == '=>':
        return Implies(*args)
    elif op == '<=>':
        return Iff(*args)

    return None


def arguments(expr):
    if isinstance(expr, Unary):
        return [expr.operand]
    elif isinstance(expr, Binary):
        return [expr.left, expr.right]

    return []
