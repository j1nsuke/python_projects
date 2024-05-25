import calendar
import datetime
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
class Target_year_month:
    def __init__(self, year: int, month: int):
        self.year = year
        self.month = month


weekday_target_counts = {
    Section.ICU: 3,
    Section.ER: 3,
    Section.NER: 3,
    Section.EICU: 3
}
weekend_target_counts = {
    Section.ICU: 2,
    Section.ER: 3,
    Section.NER: 3,
    Section.EICU: 3
}

intern_count = {
    Role.ICU: 5,
    Role.ER: 15
}

target_ym = Target_year_month(2024, 6)

def intern_counter(request_list):
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
    


def work_count_calculator(target_ym: Target_year_month, intern_count):
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
 


'''
work_counts = {
    Role.ER: {
        Section.EICU: 6,
        Section.ER: 6,
        Section.NER: 6
    },
    Role.ICU: {
        Section.ICU: 17,
        Section.NER: 3
    }
}
'''
