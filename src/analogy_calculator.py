from trace import Trace

from transformation import Transformation


class AnalogyCalculator:
    def __init__(self, model):
        self.model = model

    def find_analogy(self, A, B, C):
        a = tokenize_sentence(A.lower())
        b = tokenize_sentence(B.lower())
        c = tokenize_sentence(C.lower())
        trace_ab = Trace.calculate_trace(a, b, self.model)
        trace_ac = Trace.calculate_trace(a, c, self.model)
        D = self._calculate_analogy(c, trace_ab, trace_ac)
        return D

    def _calculate_analogy(self, s3, trace1, trace2):
        t1 = self._process_trace(trace1)
        t2 = self._process_trace(trace2, reverse=True)
        s1, s2, s3, adds = self._transform_sentences(t1, t2, s3)
        return self._compute_analogies(s1, s2, s3, adds)

    def _transform_sentences(self, t1, t2, s3):
        d = self._transform_sentence(t2, s3)
        s2, s1, prods = self._transform_grouped_sentence(t1, d)
        s3 = self._get_first(t2, s1)
        return s1, s2, s3, prods

    def _compute_analogies(self, s1, s2, s3, adds):
        result = []
        prod_idx = 0
        i = 0
        while i < len(s1):
            prod = adds[prod_idx]
            prod_idx += 1
            if len(prod.left) == 0:
                result.extend([[x] for x in prod.right])
            else:
                result_words = [x[0] for x in self.model.predict_word(s1[i], s2[i], s3[i])]
                result.append(result_words)
                i += 1
        print(result)
        return result

    def _get_first(self, t, s):
        rt = [x.reverse() for x in t]
        res1 = []
        tid = 0
        for g in s:
            l, h = 0, 0
            x = []
            try:
                while h <= len(g):
                    trans = rt[tid]
                    while len(trans.left) == 0:
                        tid += 1
                        trans = rt[tid]
                    while not trans.matches(g[l:h]) and h <= len(g):
                        h += 1
                    r = trans.transform(g[l:h])
                    x.append(r[1][0])
                    tid += 1
                    l = h
            except Exception:
                pass
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
            sl = sh
            sh += 1
            idx += 1
        return transformed

    def _transform_grouped_sentence(self, t, s):
        flat_s = [item for sublist in s for item in (sublist if type(sublist) is list else [sublist])]
        idx = 0
        sl, sh = 0, 0
        transformed = []
        lefts = []
        try:
            while sh <= len(flat_s):
                while not t[idx].matches(flat_s[sl:sh]):
                    sh += 1
                tr = t[idx].transform(flat_s[sl:sh])
                transformed.append(tr)
                lefts.append(tr[0])
                sl = sh
                idx += 1
        except IndexError:
            pass
        s1 = []
        while len(lefts) > 0:
            if lefts[0] == s[0]:
                s1.append(lefts[0])
                lefts = lefts[1:]
                s = s[1:]
            elif len(lefts[0]) > len(s[0]):
                s1.append(lefts[0])
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
                s1.append(s[0])
                exp_len = len(s[0])
                s = s[1:]
                while exp_len > 0:
                    if len(lefts[0]) < exp_len:
                        exp_len -= len(lefts[0])
                        lefts = lefts[1:]
                    else:
                        lefts = lefts[exp_len:]
                        exp_len = 0
        s2 = []
        tid = 0
        prods = []
        for g in s1:
            l, h = 0, 0
            x = []
            while h <= len(g):
                try:
                    trans = t[tid]
                    while len(trans.left) == 0:
                        prods.append(trans)
                        tid += 1
                        trans = t[tid]
                except IndexError:
                    break
                while not trans.matches(g[l:h]) and h <= len(g):
                    h += 1
                try:
                    r = trans.transform(g[l:h])
                    prods.append(Transformation([r[1][0]], [r[1][0]]))
                    x.append(r[1][0])
                    tid += 1
                    l = h
                except Exception:
                    pass
            s2.append(x)
        return s2, s1, prods

    def _process_trace(self, t, reverse=False):
        l1 = len(t.trace)
        l2 = len(t.trace[0])
        swap_groups = []
        cols_used = set()
        for i in range(l1 - 1):
            prev_row = -1
            for j in range(l2 - 1):
                if t.trace[i][j]:
                    if prev_row != i:
                        if j not in cols_used:
                            if reverse:
                                grp = Transformation([t.s2[i]], [t.s1[j]])
                                cols_used.add(j)
                            else:
                                grp = Transformation([t.s1[j]], [t.s2[i]])
                                cols_used.add(j)
                            swap_groups.append(grp)
                            prev_row = i
                        else:
                            if reverse:
                                grp = Transformation([t.s1[j]], [])
                            else:
                                grp = Transformation([], [t.s2[i]])
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
