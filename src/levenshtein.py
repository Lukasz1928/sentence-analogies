

def levenshtein(s1, s2, model):
    rows = calculate_costs(s1, s2, model)
    edits, trace = backtrace(s1, s2, rows)
    # for x in trace:
    #     for y in x:
    #         print('#' if y else ' ', end='')
    #     print()
    return rows[-1][-1], edits, trace


def calculate_costs(s1, s2, model):
    rows = []
    previous_row = range(len(s2) + 1)
    rows.append(list(previous_row))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # calculate_word_amplitude(model.get_word_vector(c1))
            deletions = current_row[j] + 1 # calculate_word_amplitude(model.get_word_vector(c2))
            substitutions = previous_row[j] + (c1 != c2) # word_distance(model.get_word_vector(c1), model.get_word_vector(c2))
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
        rows.append(previous_row)
    return rows


def backtrace(s1, s2, rows):
    i, j = len(s1), len(s2)
    edits = []
    trace = [[False] * (len(s1) + 1) for _ in range(len(s2) + 1)]
    while not (i == 0 and j == 0):
        prev_cost = rows[i][j]
        neighbors = []

        if i != 0 and j != 0:
            neighbors.append(rows[i - 1][j - 1])
        if i != 0:
            neighbors.append(rows[i - 1][j])
        if j != 0:
            neighbors.append(rows[i][j - 1])

        min_cost = min(neighbors)
        # print(neighbors)

        if min_cost == prev_cost:
            i, j = i - 1, j - 1
            edits.append({'type': 'match', 'i': i, 'j': j})
        elif i != 0 and j != 0 and min_cost == rows[i - 1][j - 1]:
            i, j = i - 1, j - 1
            edits.append({'type': 'substitution', 'i': i, 'j': j})
        elif j != 0 and min_cost == rows[i][j - 1]:
            i, j = i, j - 1
            edits.append({'type': 'insertion', 'i': i, 'j': j})
        elif i != 0 and min_cost == rows[i - 1][j]:
            i, j = i - 1, j
            edits.append({'type': 'deletion', 'i': i, 'j': j})
        trace[j][i] = True

    edits.reverse()
    return edits, trace

