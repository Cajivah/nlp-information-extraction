from abc import abstractmethod, ABCMeta


class InformationExtractor(metaclass=ABCMeta):

    def extract_all(self, list_data: list):
        if type(list_data) is not list:
            raise TypeError('First argument has to by type list')

        return [self.extract(data) for data in list_data]

    def extract(self, data):
        extracted_meta = {'subject': self.extract_subject(data),
                          'rent': self.extract_rent(data),
                          'bills': self.extract_bills(data),
                          'deposit': self.extract_deposit(data),
                          'internetSpeed': self.extract_internet_speed(data),
                          'district': self.extract_district(data),
                          'street': self.extract_street(data),
                          'roomsCount': self.extract_rooms_count(data),
                          'flatmatesCount': self.extract_flatmates_count(data),
                          'flatmatesGenders': self.extract_flatmates_gender(data),
                          'flatmatesOccupation': self.extract_flatmates_occupation(data),
                          'preferredOccupation': self.extract_preferred_gender(data),
                          'preferredGender': self.extract_preferred_gender(data)}
        return extracted_meta

    @abstractmethod
    def extract_room_meterage(self, data):
        pass

    @abstractmethod
    def extract_rent(self, data):
        pass

    @abstractmethod
    def extract_bills(self, data):
        pass

    @abstractmethod
    def extract_deposit(self, data):
        pass

    @abstractmethod
    def extract_internet_speed(self, data):
        pass

    @abstractmethod
    def extract_district(self, data):
        pass

    @abstractmethod
    def extract_street(self, data):
        pass

    @abstractmethod
    def extract_rooms_count(self, data):
        pass

    @abstractmethod
    def extract_flatmates_count(self, data):
        pass

    @abstractmethod
    def extract_flatmates_gender(self, data):
        pass

    @abstractmethod
    def extract_flatmates_occupation(self, data):
        pass

    @abstractmethod
    def extract_preferred_occupation(self, data):
        pass

    @abstractmethod
    def extract_preferred_gender(self, data):
        pass
