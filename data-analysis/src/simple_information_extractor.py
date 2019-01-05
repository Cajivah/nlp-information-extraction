from src.information_extractor import InformationExtractor
from src.morf_utils import MorfWrapper
import morfeusz2


class SimpleInformationExtractor(InformationExtractor):

    def extract_subject(self, data):
        morf = morfeusz2.Morfeusz()
        analysis = morf.analyse(data)
        morf_wrapper = MorfWrapper(analysis)

        if is_room(morf_wrapper) and not is_room_share(morf_wrapper):
            return "room"
        elif is_room_share(morf_wrapper):
            return "roomShare"
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


def is_room(morf_wrapper):
    limit = 30
    if (morf_wrapper.contains_any(['jednoosobowy', '1os', '1-os', '1-osobowy'], limit)
            or (morf_wrapper.contains('pokój', limit))):
        return True
    return False


def is_room_share(morf_wrapper):
    limit = 30
    if morf_wrapper.contains_any(['dwuosobowy', '2os', '2-os', '2-osobowy'], limit) \
            or morf_wrapper.x_before_y('miejsce', 'w', limit) \
            or morf_wrapper.x_follows_number('osobowy', 2, limit):
        return True
    return False
