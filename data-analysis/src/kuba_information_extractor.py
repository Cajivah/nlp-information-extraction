from src.information_extractor import InformationExtractor
from src.morf_utils import MorfWrapper
from src.compare_utils import deogonkify
import morfeusz2
import json
from collections import defaultdict


class KubaInformationExtractor(InformationExtractor):

    def extract_subject(self, data):
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

    def normalize_text(self, text):
        return deogonkify(text).lower()

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
