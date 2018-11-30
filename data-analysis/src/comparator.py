from collections import Counter


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
