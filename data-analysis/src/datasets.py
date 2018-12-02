import glob
import json
import os


attributes = ['subject', 'rent', 'bills', 'deposit', 'internetSpeed', 'district', 'street',
              'roomsCount', 'flatmatesCount', 'flatmatesGenders',  'flatmatesOccupation',
              'preferredOccupation',  'preferredGender']


def load(json_dir_name):
    json_pattern = os.path.join(json_dir_name, '*.json')
    data = []
    files = glob.glob(json_pattern)
    for file in files:
        with open(file) as json_data:
            classified_json = json.load(json_data)
            data.append(classified_json)
    return data
