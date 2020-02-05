from trace import Trace

from analogy_calculator import AnalogyCalculator
from levenshtein import levenshtein
from model import WordVectorModel

import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--A', type=str, nargs='+', help='First sentence', required=True)
    parser.add_argument('--B', type=str, nargs='+', help='Second sentence', required=True)
    parser.add_argument('--C', type=str, nargs='+', help='Third sentence', required=True)

    args = parser.parse_args()

    return args.A[0], args.B[0], args.C[0]


def main():
    # TODO: Use when everything is done
    # args = parse_args()
    # sentenceA, sentenceB, sentenceC = args

    model = WordVectorModel()
    calculator = AnalogyCalculator(model)

    sentenceA = "You will see the man next week."
    sentenceB = "I saw the woman last week."
    sentenceC = "You will meet the King tomorrow."

    a = "You saw the man last week."
    b = "I will see the woman next week."
    c = "You met the King yesterday."

    sentenceD = calculator.find_analogy(a, b, c)
    print(sentenceD)


if __name__ == "__main__":
    main()
