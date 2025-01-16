from datetime import datetime, time

class DateTimeManager:

    @staticmethod
    def isDateValid(date_string):
        try:
            datetime.strptime(date_string, f"%d%m%Y")
            return True  # La date est valide
        except ValueError:
            return False  # La date est invalide
        
    @staticmethod
    def isTimeValid(time_string):
        try:
            datetime.strptime(time_string, f"%H%M")
            return True  # La date est valide
        except ValueError:
            return False  # La date est invalide