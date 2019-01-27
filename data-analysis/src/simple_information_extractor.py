import re

import morfeusz2

from src.information_extractor import InformationExtractor
from src.morf_utils import MorfWrapper
from src.regex import non_alphabetic


class SimpleInformationExtractor(InformationExtractor):

    MIN_FLAT_METERAGE = 40
    MAX_ROOM_METERAGE = 30
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
        return None

    def extract_district(self, data):
        return None

    def extract_street(self, data):
        return None

    def extract_rooms_count(self, data):
        return None

    def extract_flatmates_count(self, data):
        return None

    def extract_flatmates_gender(self, data):
        return None

    def extract_flatmates_occupation(self, data):
        return None

    def extract_preferred_occupation(self, data):
        return None

    def extract_preferred_gender(self, data):
        return None


def is_room_basic(morf_wrapper):
    limit = 30
    if morf_wrapper.x_before_y('pokój', 'jednoosobowy', limit):
        return True
    if morf_wrapper.contains_any(['jednoosobowy', 'jedynka', '1os', '1-os', '1-osobowy'], limit):
        return True
    return False


def is_room(morf_wrapper):
    limit = 30
    if (morf_wrapper.contains('pokój', limit)):
        return True
    return False


def is_room_share(morf_wrapper):
    limit = 30
    if morf_wrapper.contains_any(['dwuosobowy', 'dwójka', '2os', '2-os', '2-osobowy'], limit) \
            or morf_wrapper.x_before_y('miejsce', 'w', limit) \
            or morf_wrapper.x_follows_number('osobowy', 2, limit):
        return True
    return False
