from src.information_extractor import InformationExtractor
from src.morf_utils import MorfWrapper
import pickle
import json
from src.compare_utils import deogonkify
from collections import defaultdict
import morfeusz2
import re
from src.regex import non_alphabetic


class FinalExtractor(InformationExtractor):

    MIN_FLAT_METERAGE = 40
    MAX_ROOM_METERAGE = 35
    MAX_FLAT_METERAGE = 180
    value_regex = r'[1-9][0-9]{0,2}(?:[,.][0-9])?'
    unit_regex = r'(?:m[ ^]?[2²]|mkw|mk2)' + non_alphabetic
    meterage_regex = r'(({}) ?{})'.format(value_regex, unit_regex)
    alt_meterage_regex = r'(({}) ?m){}'.format(value_regex, non_alphabetic)
    meterage_pattern = re.compile(meterage_regex)
    alt_meterage_pattern = re.compile(alt_meterage_regex)

    def extract_subject(self, data):
        morf = morfeusz2.Morfeusz()
        analysis = morf.analyse(data)
        morf_wrapper = MorfWrapper(analysis)

        if is_room_basic(morf_wrapper):
            return "room"
        elif is_room_share(morf_wrapper):
            return "roomShare"
        elif is_room(morf_wrapper):
            return "room"
        return None

    def extract_flat_meterage(self, data):
        return self.extract_meterage(data, r'mieszkanie', self.MIN_FLAT_METERAGE, self.MAX_FLAT_METERAGE)

    def extract_room_meterage(self, data):
        return self.extract_meterage(data, r'[Pp]ok[oó]j', max_val=self.MAX_ROOM_METERAGE)

    def extract_meterage(self, data, preceding, min_val=1, max_val=99999):
        match = self.meterage_pattern.findall(data)
        if match:
            for text, value in match:
                value = value.replace(',', '.')
                value = float(value)
                if min_val <= value <= max_val:
                    return value

        search_distance = 5
        match = self.alt_meterage_pattern.findall(data)
        if match:
            for text, value in match:
                value = value.replace(',', '.')
                value = float(value)
                if min_val <= value <= max_val:
                    analysis = morfeusz2.Morfeusz().analyse(data)
                    mf = MorfWrapper(analysis)
                    text = text.split(' ')
                    text = [text[0], 'metr'] if len(text) > 1 else text
                    if mf.x_before_y_within_max_distance(preceding, text, search_distance):
                        return value
        return None

    def extract_rent(self, data):
        return None

    def extract_bills(self, data):
        return None

    def extract_deposit(self, data):
        return None

    def extract_internet_speed(self, data):
        regexp = '([0-9]+)\s*[MGK][B]/*[S]*'
        speeds_found = re.findall(regexp, data, flags=re.IGNORECASE)
        if not speeds_found:
            return None

        count = defaultdict(int)
        for speed in speeds_found:
            count[speed] += 1

        sorted_by_value = sorted(count.items(), key=lambda kv: kv[1])
        return int(sorted_by_value[0][0])

    def extract_district(self, data):
        with open("./data/districts/districts.json", encoding="utf-8") as file:
            districts_data = json.load(file)
        morf = morfeusz2.Morfeusz()
        morf_analysis = morf.analyse(data)
        wrap = MorfWrapper(morf_analysis)
        by_segment = wrap.group_lemma_token_by_segment()
        norm_districts = self.normalize_districts(districts_data)
        norm_segments = self.normalize_lemmas(by_segment)
        norm_text = self.normalize_text(data)

        count = defaultdict(int)

        for segment in norm_segments:
            for lemma in segment:
                if lemma in norm_districts:
                    count[lemma] += 1

        for district in norm_districts.keys():
            if len(district.split(" ")) > 1 and district in norm_text:
                count[district] += 1

            for prefix in ['osiedle ', 'dzielnica ']:
                if prefix + district in norm_text:
                    count[district] += 100 * len(district.split(" "))

        sorted_ = [k for k, v in sorted(count.items(), key=lambda kv: (kv[1], len(kv[0].split(" "))), reverse=True)]
        return norm_districts[sorted_[0]] if len(sorted_) > 0 else None

    def normalize_lemmas(self, segments):
        norm_segments = []

        for segment in segments:
            norm_segment = []
            for lemma in segment:
                deogonkified = deogonkify(lemma)
                norm_segment.append(deogonkified.lower())
            norm_segments.append(norm_segment)

        return norm_segments

    def normalize_districts(self, districts):
        districts_dict = {}
        for district in districts:
            deogonkified = deogonkify(district)
            lower = deogonkified.lower()
            districts_dict[lower] = district

        return districts_dict

    def deogonkify_districts(self, districts):
        districts_dict = {}
        for district in districts:
            deogonkified = deogonkify(district)
            districts_dict[deogonkified] = district

        return districts_dict

    def normalize_text(self, text):
        return deogonkify(text).lower()

    def extract_street(self, data):
        with open("./data/streets/data.json", encoding="utf-8") as file:
            streets_data = json.load(file)
        streets = self.normalize_districts(streets_data)
        text = deogonkify(data).lower()

        street_to_index = defaultdict(int)
        ul_index = re.search("([\s](((ul|pl|al)(\.|\s))|(ulic|plac|alei|aleja)))", text, flags=re.IGNORECASE)
        if ul_index:
            ul_index = ul_index.start()
            probably_ul = text[ul_index:(ul_index + 40)]
            for street in streets.keys():
                street_no_suffix = street
                if street[-1:] == 'a':
                    street_no_suffix = street[:-1]
                if street_no_suffix in probably_ul:
                    self.add_street_to_count(street_to_index, probably_ul, street, street_no_suffix)
            if len(street_to_index) > 0:
                return streets[self.get_earliest_longest_street(street_to_index)]

        return None

    def add_street_to_count(self, count, probably_ul, street, street_no_suffix):
        street_index = probably_ul.index(street_no_suffix)
        count[street] = count[street] if (
                count[street] != 0 & (count[street] < street_index)) else street_index

    def get_earliest_longest_street(self, data):
        sorted_by_value = [k for k, v in sorted(data.items(), key=lambda kv: (kv[1], -len(kv[0])), reverse=False)]
        return sorted_by_value[0]

    def extract_rooms_count(self, data):

        normalized = deogonkify(data).lower()

        count_to_keyword = {
            6: ['(6((\s*)(-|–|\')*(\s*)cio)*|szesc)'],
            5: ['(5((\s*)(-|–|\')*(\s*)cio)*|piec)'],
            4: ['(cztero|4((\s*)(-|–|\')*(\s*)ro)*|czterech|cztery)'],
            3: ['(trzy|3(\s*)(-|–|\')*(\s*)|trzech)'],
            2: ['(dwu|2(\s*)(-|–|\')*(\s*)|dwoch|dwa)']
        }

        tail_regex = '(\s*)((-|–)*|(\w*))(\s*)(pokojow|pok(\s|.|,)|pokoi)'
        head_regex = '(\s|\.)'

        for count in count_to_keyword.keys():
            for keyword_regex in count_to_keyword[count]:
                if re.search(head_regex + keyword_regex + tail_regex, normalized):
                    return count

        return None

    def extract_flatmates_count(self, data):
        return None

    def extract_flatmates_gender(self, data):
        return None

    def extract_flatmates_occupation(self, data):
        return None

    def extract_preferred_occupation(self, data):
        translation = {"0": "any", "1": "professional", "2": "student"}
        with open('classifier_occupation.pickle', 'rb') as training_model:
            model = pickle.load(training_model)

        with open('tfidf_occupation.pickle', 'rb') as tfidf_model:
            tfidf = pickle.load(tfidf_model)

        prepared = tfidf.transform([data])
        prediction = model.predict(prepared)
        result = translation[str(prediction[0])]

        return result if not result == "any" else None

    def extract_preferred_gender(self, data):
        translation = {"1": "female", "2": "male", "0": "any"}
        with open('classifier_gender.pickle', 'rb') as training_model:
            model = pickle.load(training_model)

        with open('tfidf_gender.pickle', 'rb') as tfidf_model:
            tfidf = pickle.load(tfidf_model)

        prepared = tfidf.transform([data])
        prediction = model.predict(prepared)
        result = translation[str(prediction[0])]

        return result if not result == "any" else None


def is_room_basic(morf_wrapper):
    limit = 30
    if morf_wrapper.x_before_y('pokój', 'jednoosobowy', limit):
        return True
    if morf_wrapper.contains_any(['jednoosobowy', 'jedynka', '1os', '1-os', '1-osobowy'], limit):
        return True
    return False


def is_room(morf_wrapper):
    limit = 30
    if morf_wrapper.contains('pokój', limit):
        return True
    return False


def is_room_share(morf_wrapper):
    limit = 30
    if morf_wrapper.contains_any(['dwuosobowy', 'dwójka', '2os', '2-os', '2-osobowy'], limit) \
            or morf_wrapper.x_before_y('miejsce', 'w', limit) \
            or morf_wrapper.x_follows_number('osobowy', 2, limit):
        return True
    return False
