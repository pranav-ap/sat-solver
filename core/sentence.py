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


true_symbol = Symbol(True)
false_symbol = Symbol(False)


class Unary(Expression):
    def __init__(self, op, operand):
        if operand == True:
            operand = true_symbol
        elif operand == False:
            operand = false_symbol

        self.op = op
        self.operand = operand

    # repr

    def __str__(self):
        return ' '.join([self.op, str(self.operand)])


class Negate(Unary):
    def __init__(self, operand):
        super().__init__('~', operand)

    # Operator overloads

    def __invert__(self):
        return Negate('~', self)

    def __and__(self, rhs):
        return And(self, rhs)

    def __or__(self, rhs):
        return Or('|', self, rhs)

    def __rshift__(self, rhs):
        return Implies('>>', self, rhs)

    def __mod__(self, rhs):
        return Iff('==', self, rhs)

    # Reverse operator overloads

    def __rand__(self, lhs):
        return And('&', lhs, self)

    def __ror__(self, lhs):
        return Or('|', lhs, self)

    def __rrshift__(self, lhs):
        return Implies('>>', lhs, self)

    def __mod__(self, rhs):
        return Iff('==', self, rhs)


class Binary(Expression):
    def __init__(self, op, left, right):
        if left == True:
            left = true_symbol
        elif left == False:
            left = false_symbol

        if right == True:
            right = true_symbol
        elif right == False:
            right = false_symbol

        self.op = op
        self.left = left
        self.right = right

    # repr

    def __str__(self):
        return ' '.join([str(self.left), self.op, str(self.right)])


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
        super().__init__('>>', left, right)

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
        super().__init__('==', left, right)

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
