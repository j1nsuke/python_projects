import datetime
import calendar
import math
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
def Intern_counter(request_list):
    intern_count = {}
    er_count = 0
    icu_count = 0
    for request in request_list:
        if request.role == Role.ER:
            er_count += 1
        if request.role == Role.ICU:
            icu_count += 1
    intern_count[Role.ER] = er_count
    intern_count[Role.ICU] = icu_count
    return intern_count
def Convert_to_date(req_list, year: int, month: int):
    request_cals = []
    for item in req_list:
        ng_dates_list = [datetime.date(year, month, day) for day in item.ng_dates]
        extra_ng_dates_list = [datetime.date(year, month, day) for day in item.extra_ng_dates]
        intern_request = Request(item.name, item.role, item.paidoff, ng_dates_list, extra_ng_dates_list)
        request_cals.append(intern_request)
    return request_cals
def Work_count_calculator(target_ym: Target_year_month, intern_count, weekday_target_counts, weekend_target_counts):
    days_in_month = calendar.monthrange(target_ym.year, target_ym.month)[1]
    datelist = [datetime.date(target_ym.year, target_ym.month, day) for day in range(1,  days_in_month + 1)]

    weekday_count = 0
    weekend_count = 0
    for date in datelist:
        if date.weekday() < 5:
            weekday_count += 1
        else:
            weekend_count += 1

    total_work_count = {}
    for section in (Section.EICU, Section.ER, Section.ICU, Section.NER):
        count = weekday_count * weekday_target_counts[section] + weekend_count * weekend_target_counts[section]
        total_work_count[section] = count

    work_counts = {
        Role.ICU: {},
        Role.ER: {}
    }

    work_counts[Role.ICU][Section.ICU] = math.ceil(total_work_count[Section.ICU] / intern_count[Role.ICU])
    work_counts[Role.ICU][Section.NER] = math.floor((weekday_count - work_counts[Role.ICU][Section.ICU]) / 1.5)

    work_counts[Role.ER][Section.NER] = math.ceil((total_work_count[Section.NER] - work_counts[Role.ICU][Section.NER] * intern_count[Role.ICU]) / intern_count[Role.ER])
    work_counts[Role.ER][Section.ER] = math.floor((weekday_count - work_counts[Role.ER][Section.NER] * 1.5) / 2)
    work_counts[Role.ER][Section.EICU] = math.ceil((weekday_count - work_counts[Role.ER][Section.NER] * 1.5) / 2)
    
    for role, section_count in work_counts.items():
        for section, count in section_count.items():
            print(f"{role}-{section} = {count}")
    
    return work_counts