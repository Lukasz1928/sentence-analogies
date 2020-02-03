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
    analogy = calculator.find_analogy(' '.join(['You', 'will', 'see', 'the', 'man', 'next', 'week']), ' '.join(['I', 'saw', 'the', 'woman', 'last', 'week']),
                            ' '.join(['You', 'will', 'meet', 'the', 'King', 'tomorrow']))
    print(analogy)
    sentenceA = "You will see the man next week."
    sentenceB = "I saw the woman last week."
    sentenceC = "You will meet the King tomorrow."

    #sentenceD = calculator.find_analogy(sentenceA, sentenceB, sentenceC)
    #print(sentenceD)

    #l1 = levenshtein(['You', 'will', 'see', 'the', 'man', 'next', 'week'], ['I', 'see', 'the', 'woman', 'this', 'week'], None)

    # t1 = Trace.calculate_trace(['You', 'will', 'see', 'the', 'man', 'next', 'week'], ['I', 'saw', 'the', 'woman', 'last', 'week'], None)
    # print(t1.edits)
    # t2 = Trace.calculate_trace(['You', 'will', 'see', 'the', 'man', 'next', 'week'], ['You', 'will', 'meet', 'the', 'King', 'tomorrow'], None)
    # print(t2.edits)
    # print(l1)


if __name__ == "__main__":
    main()
