import collections
import re

class MorfWrapper:

    def __init__(self, analysis) -> None:
        self.analysis = analysis
        self.lemmas = self.group_lemma_by_segment_no_suffix()

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

    def group_lemma_by_segment_no_suffix(self):
        by_segment = self.group_by_segment()
        grouped_no_suffix = []
        for segment in by_segment:
            cores = []
            for lemma in segment:
                core = lemma.split(':')[0]
                if core not in cores:
                    cores.append(core)
            grouped_no_suffix.append(cores)

        return grouped_no_suffix

    def group_lemma_token_by_segment(self):
        grouped = collections.OrderedDict()
        for segment_start, segment_end, word in self.analysis:
            token, lemma, tags, qualifiers1, qualifiers2 = word
            core = lemma.split(':')[0]
            key = self.gen_key(segment_start, segment_end)
            if key in grouped:
                if token not in grouped[key]:
                    grouped[key].append(token)

                if core not in grouped[key]:
                    grouped[key].append(core)
            else:
                grouped[key] = [token]
                if core not in grouped[key]:
                    grouped[key].append(core)
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

    def contains_any(self, words, limit=None):
        if limit is None:
            limit = len(self.lemmas)

        for i in range(0, min(limit, len(self.lemmas)) - 1):
            if any(word in words for word in self.lemmas[i]):
                return True
        return False

    def x_before_y(self, x, y, limit=None):
        '''
        :param limit: x will be searched only in first :limit words
        '''
        if limit is None:
            limit = len(self.lemmas)

        for i in range(0, min(limit, len(self.lemmas)) - 1):
            if x in self.lemmas[i] and y in self.lemmas[i + 1]:
                return True
        return False

    def x_follows_number(self, x, number, limit=None):
        if limit is None:
            limit = len(self.lemmas)

        for i in range(0, min(limit, len(self.lemmas)) - 1):
            if number_in_collection(self.lemmas[i], number) and x in self.lemmas[i + 1]:
                return True
        return False

    def x_before_y_within_max_distance(self, x, y, distance):
        pattern = re.compile(x)
        y_index = -1
        for lemma_index in range(len(self.lemmas) - len(y)):
            for i, y_item in enumerate(y):
                if y_item not in self.lemmas[lemma_index + i]:
                    break
                if i + 1 == len(y):
                    y_index = lemma_index
                    break
        if y_index < 0:
            return False

        search_start_index = max(0, y_index - distance)
        for lemma in self.lemmas[search_start_index: y_index]:
            if any(pattern.match(l) for l in lemma):
                return True
        return False


def number_in_collection(collection, number):
    for item in collection:
        if is_number(item) and number == float(item):
            return True
    return False


def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
