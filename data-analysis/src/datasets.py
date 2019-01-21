import glob
import json
import os


attributes = ['subject', 'flatMeterage', 'roomMeterage', 'rent', 'bills', 'deposit', 'internetSpeed',
              'district', 'street', 'roomsCount', 'flatmatesCount', 'flatmatesGenders', 'flatmatesOccupation',
              'preferredOccupation', 'preferredGender']


def load(json_dir_name):
    json_pattern = os.path.join(json_dir_name, '*.json')
    data = []
    files = glob.glob(json_pattern)
    for file in files:
        with open(file, encoding='utf-8') as json_data:
            classified_json = json.load(json_data)
            data.append(classified_json)
    return data


def save_by_category(directory, data_sets, category):
    for i in range(0, len(data_sets)):
        content = data_sets[i]["content"]
        category = data_sets[i]["meta"][category]
        if category is None:
            category = 'any'
        with open(f'{directory}/{category}/{str(i)}.txt', mode='x', encoding='utf-8') as f:
            f.write(content)
    return None


def load_stopwords():
    with open('data/nltk/stopwords.json', encoding='utf-8') as f:
        return json.load(f)
