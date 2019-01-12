def count(data: list) -> dict:
    count = {}
    for metadata in data:
        for key, value in metadata['meta'].items():
            if key == 'data':
                continue
            if value is not None:
                count[key] = count.get(key, 0) + 1

    return count


def frequency(data: list) -> dict:
    frequency = count(data)
    data_count = len(data)

    for key, value in frequency.items():
        frequency[key] = round(frequency[key] / data_count, 2)

    return frequency


def sort_by_value(stats: dict) -> list:
    return sorted(stats.items(), key=lambda kv: kv[1], reverse=True)
