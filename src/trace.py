from levenshtein import levenshtein


class Trace:
    def __init__(self, s1, s2, trace, edits):
        self.s1 = s1
        self.s2 = s2

        self.trace = trace
        self.trace_elements = [(i, j) for i in range(len(trace)) for j in range(len(trace[i])) if trace[i][j]]

        self.edits = edits

    @staticmethod
    def calculate_trace(s1, s2, model):
        edits, trace_matrix = levenshtein(s1, s2, model)[1:]
        for i in reversed(range(len(trace_matrix))):
            for j in reversed(range(len(trace_matrix[i]))):
                try:
                    pass
                    if trace_matrix[i][j] and trace_matrix[i + 1][j + 1] and trace_matrix[i][j - 1] and not trace_matrix[i + 1][j] and not trace_matrix[i - 1][j]:
                        trace_matrix[i + 1][j] = True
                        trace_matrix[i][j] = False
                    # if trace_matrix[i][j] and trace_matrix[i + 1][j + 1] and not trace_matrix[i - 1][j] and not trace_matrix[i - 1][j - 1]:
                    #     trace_matrix[i + 1][j] = True
                    #     trace_matrix[i][j] = False
                except KeyError:
                    pass
        # for x in trace_matrix:
        #     for y in x:
        #         print('#' if y else ' ', end='')
        #     print()
        es = []
        # for e in edits:
        #     if e['type'] == 'match':
        #         es.append(('M', e['i'], e['j']))
        #     elif e['type'] == 'deletion':
        #         es.append(('D', e['i']))
        #     elif e['type'] == 'insertion':
        #         es.append(('I', e['i'], e['j'], s2[e['j']]))
        #     elif e['type'] == 'substitution':
        #         es.append(('S', e['i'],  e['j'], s2[e['j']]))
        return Trace(s1, s2, trace_matrix, es)
