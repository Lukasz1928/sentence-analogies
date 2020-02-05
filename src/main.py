from analogy_calculator import AnalogyCalculator
from model import WordVectorModel


def main():
    model = WordVectorModel()
    calculator = AnalogyCalculator(model)

    sentenceA = "You will see the man next week."
    sentenceB = "I saw the woman last week."
    sentenceC = "You will meet the King tomorrow."

    sentenceD = calculator.find_analogy(sentenceA, sentenceB, sentenceC)
    print(sentenceD)

    a = "You saw the man last week."
    b = "I will see the woman next week."
    c = "You met the King yesterday."

    d = calculator.find_analogy(a, b, c)
    print(d)


if __name__ == "__main__":
    main()
