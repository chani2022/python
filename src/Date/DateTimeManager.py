from datetime import datetime, time
import re

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
        pattern = r"^(?:[01]\d|2[0-3])[0-5]\d$"
        return bool(re.match(pattern,time_string))
    
    @staticmethod
    def convertStringToDate(date_string, format=f"%d%m%Y"):
        try:
            return datetime.strptime(date_string, format)
        except ValueError:
            return False  # La date est invalide
    @staticmethod
    def isYearValid(date_string):
        try:
            datetime.strptime(date_string, f"%Y")
            return True  # La date est valide
        except ValueError:
            return False  # La date est invalide
        
    @staticmethod
    def convertStringToHours(hours_string, format=f"%H%M"):
        try:
            return datetime.strptime(hours_string, format)
        except ValueError:
            return False  # La date est invalide

