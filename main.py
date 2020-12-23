from core.sentence import Symbol
from core import make_symbols


def main():
    # add sentences

    x, y = make_symbols('x y')

    s = x & y | True
    print(s)


if __name__ == '__main__':
    main()
