from abc import abstractmethod, ABCMeta


class InformationExtractor(metaclass=ABCMeta):

    def __init__(self, data):
        self.data = data

    def extract(self):
        extracted_meta = {'subject': self.extract_subject(),
                          'rent': self.extract_rent(),
                          'bills': self.extract_bills(),
                          'deposit': self.extract_deposit(),
                          'internetSpeed': self.extract_internet_speed(),
                          'district': self.extract_district(),
                          'street': self.extract_street(),
                          'roomsCount': self.extract_rooms_count(),
                          'flatmatesCount': self.extract_flatmates_count(),
                          'flatmatesGenders': self.extract_flatmates_gender(),
                          'flatmatesOccupation': self.extract_flatmates_occupation(),
                          'preferredOccupation': self.extract_preferred_gender(),
                          'preferredGender': self.extract_preferred_gender()}
        return extracted_meta

    @abstractmethod
    def extract_subject(self):
        pass

    @abstractmethod
    def extract_rent(self):
        pass

    @abstractmethod
    def extract_bills(self):
        pass

    @abstractmethod
    def extract_deposit(self):
        pass

    @abstractmethod
    def extract_internet_speed(self):
        pass

    @abstractmethod
    def extract_district(self):
        pass

    @abstractmethod
    def extract_street(self):
        pass

    @abstractmethod
    def extract_rooms_count(self):
        pass

    @abstractmethod
    def extract_flatmates_count(self):
        pass

    @abstractmethod
    def extract_flatmates_gender(self):
        pass

    @abstractmethod
    def extract_flatmates_occupation(self):
        pass

    @abstractmethod
    def extract_preferred_occupation(self):
        pass

    @abstractmethod
    def extract_preferred_gender(self):
        pass
