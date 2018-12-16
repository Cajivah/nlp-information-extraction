import collections


class MorfWrapper:

    def __init__(self, analysis) -> None:
        self.analysis = analysis
        self.lemmas = self.group_by_segment()

    def group_by_segment(self):
        grouped = collections.OrderedDict()
        for segment_start, segment_end, word in self.analysis:
            token, lemma, tags, qualifiers1, qualifiers2 = word
            key = self.gen_key(segment_start, segment_end)
            if key in grouped:
                grouped[key].append(lemma)
            else:
                grouped[key] = [lemma]
        return list(grouped.values())

    def gen_key(self, s1, s2):
        return str(s1) + str(s2)

    def contains(self, word, limit=None):
        if limit is None:
            limit = len(self.lemmas)

        for i in range(0, min(limit, len(self.lemmas)) - 1):
            if word in self.lemmas[i]:
                return True
        return False

    def x_follows_y(self, x, y, limit=None):
        '''
        :param limit: x will be searched only in first :limit words
        '''
        if limit is None:
            limit = len(self.lemmas)

        for i in range(0, min(limit, len(self.lemmas)) - 1):
            if y in self.lemmas[i] and x in self.lemmas[i + 1]:
                return True
        return False

    def x_follows_number(self, x, limit=None):
        if limit is None:
            limit = len(self.lemmas)

        for i in range(0, min(limit, len(self.lemmas)) - 1):
            if number_in_collection(self.lemmas[i]) and x in self.lemmas[i + 1]:
                return True
        return False


def number_in_collection(collection):
    for item in collection:
        if is_number(item):
            return True
    return False


def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
