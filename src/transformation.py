

class Transformation:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def matches(self, s):
        #print('matches {} {}'.format(s, self.left))
        if all([type(x) is str for x in s]):
            return s == self.left
        flat_list = [item for sublist in s for item in (sublist if type(sublist) is list else [sublist])]
        return flat_list == self.left

    def transform(self, s):
        #print('trying to transform: {} with {} -> {}'.format(s, self.left, self.right), end='')
        if self.matches(s):
            return self.left, self.right
        raise Exception("DUPA")

    def reverse(self):
        return Transformation(self.right, self.left)

    def __str__(self):
        return '{} -> {}'.format(self.left, self.right)
