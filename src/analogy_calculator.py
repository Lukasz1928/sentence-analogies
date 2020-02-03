from trace import Trace

from distance import calculate_similarity_matrix
from transformation import Transformation


class AnalogyCalculator:
    def __init__(self, model):
        self.model = model

    def find_analogy(self, A, B, C):
        a = tokenize_sentence(A.lower())
        b = tokenize_sentence(B.lower())
        c = tokenize_sentence(C.lower())
        # print(a)
        # print(b)
        # vectors_a = self.model.get_sentence_vectors(a)
        # vectors_b = self.model.get_sentence_vectors(b)
        # vectors_c = self.model.get_sentence_vectors(c)
        # similarity_matrix = calculate_similarity_matrix(vectors_a, vectors_b)
        trace_ab = Trace.calculate_trace(a, b, self.model)
        # for i in range(len(trace_ab.trace)):
        #     for j in range(len(trace_ab.trace[i])):
        #         print('#' if trace_ab.trace[i][j] else ' ', end='')
        #     print('')
        trace_ac = Trace.calculate_trace(a, c, self.model)
        D_length = len(b) - len(a) + len(c)
        D = self._calculate_analogy(a, b, c, trace_ab, trace_ac, D_length)
        return D

    def _calculate_analogy(self, s1, s2, s3, trace1, trace2, expected_length):
        result = []
        t1 = self._process_trace(trace1)
        # print([str(x) for x in t1])
        t2 = self._process_trace(trace2, reverse=True)
        # for i in range(len(trace1.trace)):
        #     for j in range(len(trace1.trace[i])):
        #         print('#' if trace1.trace[i][j] else ' ', end='')
        #     print()
        # print()
        # for i in range(len(trace2.trace)):
        #     for j in range(len(trace2.trace[i])):
        #         print('#' if trace2.trace[i][j] else ' ', end='')
        #     print()
        #print([str(x) for x in t2])
        # print(s3)

        s1, s2, s3 = self._transform_sentences(t1, t2, s3)

        return self._compute_analogies(s1, s2, s3)

    def _transform_sentences(self, t1, t2, s3):
        # print('r3: {}'.format(s3))
        d = self._transform_sentence(t2, s3)

        # print([str(x) for x in t2])

        # print('d: {}'.format(d))
        s2, x, s1 = self._transform_grouped_sentence(t1, d)

        # print('x: {}'.format(x))
        # print('s1: {}'.format(s1))
        # print('s2: ' + str(s2))

        s3 = self._get_first(t2, s1)
        # print('s3: {}'.format(s3))
        return s1, s2, s3

    def _compute_analogies(self, s1, s2, s3):
        print(len(s1), len(s2), len(s3))
        print(s1)
        print(s2)
        print(s3)
        result = []
        for i in range(len(s1)):
            result_word = self.model.predict_word([s1[i]], [s2[i]], [s3[i]])
            result.append(result_word)
        return result

    def _get_first(self, t, s):
        rt = [x.reverse() for x in t]
        res1 = []
        tid = 0
        for g in s:
            l, h = 0, 1
            x = []
            while h <= len(g):
                trans = rt[tid]
                while not trans.matches(g[l:h]):
                    h += 1
                r = trans.transform(g[l:h])
                x.append(r[1][0])
                tid += 1
                l = h
                h += 1
            res1.append(x)
        return res1

    def _transform_sentence(self, t, s):
        idx = 0
        sl, sh = 0, 1
        transformed = []

        while sh <= len(s):
            while not t[idx].matches(s[sl:sh]):
                sh += 1
            transformed.append(t[idx].transform(s[sl:sh])[1])
            #print(t[idx].transform(s[sl:sh])[1])
            sl = sh
            sh += 1
            idx += 1
        return transformed

    def _transform_grouped_sentence(self, t, s):
        flat_s = [item for sublist in s for item in (sublist if type(sublist) is list else [sublist])]
        idx = 0
        sl, sh = 0, 1
        transformed = []
        lefts = []
        while sh <= len(flat_s):
            while not t[idx].matches(flat_s[sl:sh]):
                sh += 1
            tr = t[idx].transform(flat_s[sl:sh])
            transformed.append(tr)
            lefts.append(tr[0])
            sl = sh
            sh += 1
            idx += 1
        res = []
        while len(lefts) > 0:
            if lefts[0] == s[0]:
                res.append(lefts[0])
                lefts = lefts[1:]
                s = s[1:]
            elif len(lefts[0]) > len(s[0]):
                res.append(lefts[0])
                exp_len = len(lefts[0])
                lefts = lefts[1:]
                while exp_len > 0:
                    if len(s[0]) < exp_len:
                        exp_len -= len(s[0])
                        s = s[1:]
                    else:
                        s = s[exp_len:]
                        exp_len = 0
            else:
                res.append(s[0])
                exp_len = len(s[0])
                s = s[1:]
                while exp_len > 0:
                    if len(lefts[0]) < exp_len:
                        exp_len -= len(lefts[0])
                        lefts = lefts[1:]
                    else:
                        lefts = lefts[exp_len:]
                        exp_len = 0

        res1 = []
        tid = 0
        for g in res:
            l, h = 0, 1
            x = []
            while h <= len(g):
                trans = t[tid]
                while not trans.matches(g[l:h]):
                    h += 1
                r = trans.transform(g[l:h])

                x.append(r[1][0])
                tid += 1
                l = h
                h += 1
            res1.append(x)
        return res1, [x[0] for x in transformed], res

    def _process_trace(self, t, reverse=False):
        l1 = len(t.trace)
        l2 = len(t.trace[0])
        swap_groups = []
        for i in range(l1 - 1):
            prev_row = -1
            for j in range(l2 - 1):
                if t.trace[i][j]:
                    if prev_row != i:
                        if reverse:
                            grp = Transformation([t.s2[i]], [t.s1[j]])
                        else:
                            grp = Transformation([t.s1[j]], [t.s2[i]])
                        swap_groups.append(grp)
                        prev_row = i
                    else:
                        if reverse:
                            swap_groups[len(swap_groups) - 1].right.append(t.s1[j])
                        else:
                            swap_groups[len(swap_groups) - 1].left.append(t.s1[j])

        return swap_groups


def tokenize_sentence(sentence):
    tokens = [t.strip('.,') for t in sentence.split(' ')]
    return [t for t in tokens if t.isalpha()]
