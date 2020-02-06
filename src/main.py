from analogy_calculator import AnalogyCalculator
from model import WordVectorModel


def main():
    model = WordVectorModel()
    calculator = AnalogyCalculator(model)
    print('model loaded')

    a = "You will see the man next week."
    b = "I saw the woman last week."
    c = "You will meet the King tomorrow."
    d = calculator.find_analogy(a, b, c)
    print(d)

    a = "You saw the man last week."
    b = "I will see the woman next week."
    c = "You met the King yesterday."
    d = calculator.find_analogy(a, b, c)
    print(d)


if __name__ == "__main__":
    main()
