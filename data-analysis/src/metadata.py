def count(data: list) -> dict:
    count = {}
    for metadata in data:
        for key, value in metadata['meta'].items():
            if value is not None:
                count[key] = count.get(key, 0) + 1

    return count


def frequency(data: list) -> dict:
    frequency = count(data)
    data_count = len(data)

    for key, value in frequency.items():
        frequency[key] = round(frequency[key] / data_count, 3)

    return frequency


def sort_by_value(stats: dict, reverse=False) -> list:
    return sorted(stats.items(), key=lambda kv: kv[1], reverse=reverse)


def sort_by_key(stats: dict, reverse=False) -> list:
    return sorted(stats.items(), key=lambda kv: kv[0], reverse=reverse)


def map_to_polish_names(meta: dict):
    for key, value in list(meta.items()):
        new_key = attributes_mappings[key]
        meta[new_key] = meta[key]
        del meta[key]
    return meta


attributes_mappings = {
    'subject': 'temat',
    'rent': 'czynsz',
    'street': 'ulica',
    'bills': 'rachunki',
    'roomsCount': 'liczba pokojów',
    'deposit': 'kaucja',
    'roomMeterage': 'metraż mieszkania',
    'district': 'osiedle',
    'flatmatesCount': 'liczba współlokatorów',
    'flatmatesGenders': 'płeć współlokatorów',
    'flatmatesOccupation': 'zawód współlokatorów',
    'preferredGender': 'preferowana płeć',
    'flatMeterage': 'metraż mieszkania',
    'internetSpeed': 'prędkość internetu',
    'preferredOccupation': 'preferowany zawód',
}


def files_stats(data: list) -> dict:
    stats = {}

    for metadata in data:
        metadata_count = 0
        for key, value in metadata['meta'].items():
            if value is not None:
                metadata_count += 1

        stats[metadata_count] = stats.get(metadata_count, 0) + 1

    return stats
