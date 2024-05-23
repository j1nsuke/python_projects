import datetime
from enum import Enum

class Section(Enum):
    OFF = 'OFF_'
    ER = 'ER__'
    NER = 'NER_'
    ICU = 'ICU_'
    EICU = 'EICU'
    NG_A = 'NG_A'
    NG_B = 'NG_B'
class Role(Enum):
    ER = 'ER'
    ICU = 'ICU'
class Request:
    def __init__(self, name: str, role: Role, paidoff: int, ng_dates: list, extra_ng_dates: list):
        self.name = name
        self.role = role
        self.paidoff = paidoff
        self.ng_dates = ng_dates
        self.extra_ng_dates = extra_ng_dates
class Target_year_month:
    def __init__(self, year: int, month: int):
        self.year = year
        self.month = month
def Convert_to_date(req_list, year: int, month: int):
    request_cals = []
    for item in req_list:
        ng_dates_list = [datetime.date(year, month, day) for day in item.ng_dates]
        extra_ng_dates_list = [datetime.date(year, month, day) for day in item.extra_ng_dates]
        intern_request = Request(item.name, item.role, item.paidoff, ng_dates_list, extra_ng_dates_list)
        request_cals.append(intern_request)
    return request_cals
