from collections import Counter

from src import datasets
from src.information_extractor import InformationExtractor
import pandas as pd


def compare_metadata_all(list1, list2) -> list:
    return [compare_metadata(dict1, dict2) for dict1, dict2 in zip(list1, list2)]


def compare_metadata(dict1, dict2):
    comparison = {}
    for key, value in dict1.items():
        comparison[key] = {'original': value,
                           'extracted': dict2[key],
                           'equal': compare_values(value, dict2[key])}
    return comparison


def compare_values(value1, value2):
    if type(value1) is list:
        return Counter(value1) == Counter(value2)
    return value1 == value2


def print_diff(diffs):
    for diff in diffs:
        print(diff['data'] + '\n')
        for key, value in diff['meta'].items():
            print("{} - {} / {}".format(key, value['original'], value['extracted']))
        print('\n---------------------------------------------------------\n')


def print_correctly_extracted(data_list):
    for data in data_list:
        print(data['data'] + '\n')
        for key, value in data['meta'].items():
            print("{} - {}".format(key, value))
        print('\n---------------------------------------------------------\n')


class Comparator:
    def __init__(self, datasets: list):
        self.datasets = datasets
        self.original_meta_list = [dataset['meta'] for dataset in self.datasets]
        self.data_list = [dataset['content'] for dataset in self.datasets]

    def measure_accuracy(self, extractor: InformationExtractor, attributes=datasets.attributes,
                         skip_nones=True):
        """
        :param extractor: extractor used for extracting data to compare
        :param attributes: attributes to compare, defaults to all
        :param skip_nones: indicates whether null values should be included in comparing
        """
        extracted_meta_list = extractor.extract_all(self.data_list)
        diffs = compare_metadata_all(self.original_meta_list, extracted_meta_list)
        correctly_extracted = []
        incorrectly_extracted = []
        correctly_extracted_count = 0
        incorrectly_extracted_count = 0
        for diff, data in zip(diffs, self.data_list):
            correct_meta = {}
            incorrect_meta = {}
            for key, value in diff.items():
                if self.should_be_included(key, value['original'], attributes, skip_nones):
                    if value['equal'] is True:
                        correct_meta[key] = value['original']
                    else:
                        incorrect_meta[key] = {
                            'original': value['original'],
                            'extracted': value['extracted']}
            if len(correct_meta.keys()) > 0:
                correctly_extracted.append({
                    "data": data,
                    "meta": correct_meta
                })
                correctly_extracted_count += len(correct_meta.keys())
            if len(incorrect_meta.keys()) > 0:
                incorrectly_extracted.append({
                    "data": data,
                    "meta": incorrect_meta
                })
                incorrectly_extracted_count += len(incorrect_meta.keys())
        accuracy = correctly_extracted_count / (correctly_extracted_count + incorrectly_extracted_count)
        return accuracy, correctly_extracted, incorrectly_extracted

    def should_be_included(self, key, value, attributes, skip_nones):
        if skip_nones is True:
            return True if key in attributes and value is not None else False
        else:
            return True if key in attributes else False

    def get_all_measures(self, extractor: InformationExtractor, attributes=datasets.attributes):
        score = Score()
        extracted_meta_list = extractor.extract_all(self.data_list)
        diffs = compare_metadata_all(self.original_meta_list, extracted_meta_list)
        for diff in diffs:
            for key, value in diff.items():
                if self.should_be_included(key, value['original'], attributes, skip_nones=False):
                    extracted = value['original']
                    original = value['original']

                    if value['equal'] is True:
                        score.inc_correctly_extracted()
                        if original is None:
                            score.inc_true_negative()
                        else:
                            score.inc_true_positive()
                    else:
                        score.inc_incorrectly_extracted()
                        if (extracted is None and original is not None) or (extracted is not None and original is not None):
                            score.inc_false_negative()
                        else:
                            score.inc_false_positive()
        return score


class Score:

    def __init__(self):
        self.accuracy = 0
        self._correctly_extracted = 0
        self._incorrectly_extracted = 0
        self.true_positive = 0
        self.true_negative = 0
        self.false_positive = 0
        self.false_negative = 0

    def inc_correctly_extracted(self):
        self._correctly_extracted += 1
        self.accuracy = self._correctly_extracted / (self._correctly_extracted + self._incorrectly_extracted)

    def inc_incorrectly_extracted(self):
        self._incorrectly_extracted += 1
        self.accuracy = self._correctly_extracted / (self._correctly_extracted + self._incorrectly_extracted)

    def inc_true_positive(self):
        self.true_positive += 1

    def inc_true_negative(self):
        self.true_negative += 1

    def inc_false_positive(self):
        self.false_positive += 1

    def inc_false_negative(self):
        self.false_negative += 1


def get_confusion_matrix(score: Score):
    confusion_matrix =  [
        [score.true_positive, score.false_negative],
        [score.false_positive, score.true_negative]
    ]
    return pd.DataFrame(confusion_matrix, index= ["Zawarte", "Niezawarte"], \
                                        columns=["Wydobyte", "Niewydobyte"])

