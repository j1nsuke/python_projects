import datetime
from enum import Enum

# カレンダーの用意
cal_begin   = datetime.date(2024,7,1)
cal_end     = datetime.date(2024,9,30)
target_cal  = [cal_begin + datetime.timedelta(days = i) for i in range (0, (cal_end - cal_begin).days + 1)]

class Time(Enum):
    day = "日勤"
    night = "夜勤"
    extra = "外勤"
class Section(Enum):
    s30591 = "30591"
    s30595 = "30595"
    s30599 = "30599"
    s30596 = "30596"
    s30597 = "30597"
    sIsub1 = "Isub1"
    sIsub2 = "Isub2"
    s30594 = '30594'
    sEsub1 = "Esub1"
    sEsub2 = "Esub2"

    OFF    = "OFF"
    NG     = "NG"

    sonoda = "苑田"
    teikyo = "帝京"
    mitsui = "三井"
    oomori = "大森"
    taitou = "台東"
    chibat = "千葉徳"
    extras = "個人外勤"
time_section = {
        Time.day: (Section.s30591, Section.s30595, Section.s30599, Section.s30594, Section.sEsub1, Section.sEsub2, Section.s30596, Section.s30597, Section.sIsub1, Section.sIsub2),
        Time.night: (Section.s30595, Section.s30599, Section.s30596),
        Time.extra: (Section.sonoda, Section.teikyo, Section.mitsui, Section.taitou, Section.oomori, Section.chibat, Section.extras)
}

class Staff():
    def __init__(self, name, rank, is_phd = False, certified_section = [],  ng_request = []):
        self.name = name
        self.rank = rank
        self.certified_section = certified_section
        self.ng_request = ng_request if ng_request is not None else []
        self.is_phd = is_phd
        self.work_count = 0
        self.extra_count = 0
        self.personal_schedule = {date: {Time.day: Section.OFF, Time.night: Section.OFF} for date in target_cal}
        self.personal_schedule.update({date: {Time.day: Section.NG, Time.night: Section.NG} for date in ng_request})
    def available(self, date, time) -> bool:
        previous_date = date - datetime.timedelta(days = 1) if date != cal_begin else None
        next_date = date + datetime.timedelta(days = 1) if date != cal_end else None
        if time == Time.day:
            return all([self.personal_schedule[previous_date][Time.night] == Section.OFF if previous_date else True,
                self.personal_schedule[date][Time.day] == Section.OFF])
        elif time == Time.night:
            return all([self.personal_schedule[previous_date][Time.night] == Section.OFF if previous_date else True,
                self.personal_schedule[date][Time.night] == Section.OFF,
                self.personal_schedule[next_date][Time.day] == Section.OFF if next_date else True,
                self.personal_schedule[next_date][Time.night] == Section.OFF if next_date else True,
                ])
    def available_days(self, date):
        count = 0
        check_date = date
        while check_date <= cal_end:
            if self.available(check_date, Time.day) and self.available(check_date, Time.night):
                count += 1
                check_date += datetime.timedelta(days = 1)
            else:
                break
        return count

# スタッフ名簿
staffs = [
    Staff("浅田",   rank=16,    ng_request = [datetime.date(2024,7,2),datetime.date(2024,7,7),datetime.date(2024,9,14)] + [date for date in target_cal if date.weekday() == 2]), #毎週水曜外勤
    Staff("山本",   rank=16,    ng_request = [datetime.date(2024,7,4),datetime.date(2024,8,24),]),
    Staff("和田",   rank=18,    certified_section = [Section.s30594, Section.s30595], ng_request =[datetime.date(2024,7,4),datetime.date(2024,7,10),datetime.date(2024,7,11),datetime.date(2024,7,13),datetime.date(2024,7,18),datetime.date(2024,7,19),datetime.date(2024,7,20),datetime.date(2024,7,21),datetime.date(2024,7,31)]+[date for date in target_cal if date.weekday() == 1]), #毎週火曜外勤
    Staff("堀江",   rank=17,    certified_section = [Section.s30594, Section.s30595], ng_request =[datetime.date(2024,7,7),datetime.date(2024,7,13),datetime.date(2024,8,11)]),
    Staff("佐藤拓", rank=12,    certified_section = [Section.s30594, Section.s30595], ng_request =[datetime.date(2024,7,6),datetime.date(2024,7,15),datetime.date(2024,7,16),datetime.date(2024,8,20),]+[date for date in target_cal if date.weekday() == 4], is_phd = True),#毎週金曜外勤
    Staff("田上",   rank=12,    certified_section = [Section.s30594, Section.s30595], ng_request =[datetime.date(2024,8,25)]+[date for date in target_cal if date.weekday() in (1,4)], is_phd = True),
    Staff("高井",   rank=10,    certified_section = [Section.s30594, Section.s30595, Section.s30596], ng_request =[datetime.date(2024,8,16),datetime.date(2024,8,17),datetime.date(2024,8,18),datetime.date(2024,8,19),datetime.date(2024,8,20),datetime.date(2024,8,21),datetime.date(2024,7,27),datetime.date(2024,7,28),datetime.date(2024,8,24),datetime.date(2024,8,25),datetime.date(2024,9,28),datetime.date(2024,9,29),], is_phd = True),
    Staff("水野",   rank=10,    certified_section = [Section.s30594, Section.s30595, Section.s30596], ng_request =[date for date in target_cal if date.weekday() in (3,4)], is_phd = True),#毎週木曜外勤 +金曜明け
    Staff("佐藤悠", rank= 8,    certified_section = [Section.s30594, Section.s30595, Section.s30596], ng_request =[datetime.date(2024,9,1)]),
    Staff("中野",   rank= 6,    certified_section = [Section.s30594, Section.s30595, Section.s30596], ng_request =[datetime.date(2024,9,14)]),
    Staff("木村",   rank= 6,    certified_section = [Section.s30594, Section.s30595, Section.s30596], ng_request =[datetime.date(2024,7,21),datetime.date(2024,8,4),datetime.date(2024,8,24),datetime.date(2024,9,1),datetime.date(2024,9,14),datetime.date(2024,9,24),]),
    Staff("有田",   rank= 6,    certified_section = [Section.s30594, Section.s30595], ng_request =[datetime.date(2024,8,31),datetime.date(2024,9,14),datetime.date(2024,9,27),]),
    Staff("佐藤一", rank= 5,    certified_section = [Section.s30594, Section.s30595, Section.s30596], ng_request =[datetime.date(2024,7,16),datetime.date(2024,8,2),datetime.date(2024,8,9),datetime.date(2024,8,16),datetime.date(2024,8,19),datetime.date(2024,8,24),datetime.date(2024,8,25),]),
    Staff("堂園",   rank= 5,    certified_section = [Section.s30594, Section.s30595], ng_request =[datetime.date(2024,7,7),datetime.date(2024,9,8),]),
    Staff("池上",   rank= 4,    certified_section = [Section.s30594], ng_request =[datetime.date(2024,7,28),datetime.date(2024,8,4),datetime.date(2024,8,8),datetime.date(2024,8,18),datetime.date(2024,8,30),datetime.date(2024,9,1),datetime.date(2024,9,8),]),
    Staff("谷本",   rank= 4,    ng_request = [date for date in target_cal if date.weekday() == 5]), #毎週金夜が外勤
    Staff("川上",   rank= 3,    ng_request = [datetime.date(2024,7,18),datetime.date(2024,7,19),]),
    Staff("河田",   rank= 3,    ng_request = [datetime.date(2024,7,1),datetime.date(2024,7,18),datetime.date(2024,7,19),datetime.date(2024,9,22),]),
    Staff("諏江",   rank= 3,    ng_request = [datetime.date(2024,7,1),datetime.date(2024,7,6),datetime.date(2024,7,18),datetime.date(2024,7,19),datetime.date(2024,8,24),datetime.date(2024,9,8),]),
    Staff("松山",   rank= 3,    ng_request = [datetime.date(2024,7,18),datetime.date(2024,7,19)]),
    Staff("野田",   rank= 3,    ng_request = [datetime.date(2024,7,13),]),
    Staff("瀧",     rank= 4,    ng_request = [datetime.date(2024,7,27),datetime.date(2024,8,10),datetime.date(2024,9,27),datetime.date(2024,9,28)]),
    # Staff("Kobayasi", rank= 3,    ng_request =[]),
    # Staff("Ikeda",    rank= 5,    ng_request =[]),
]
def print_ng_count(staffs):
    print("PRINT TOO MUCH NGs on...")
    for date in target_cal:
        count = 0
        for staff in staffs:
            if date in staff.ng_request:
                count += 1
        if count > 4:
            print(f"{date}, ng={count}")
def get_staff_by_name(name):
    return next((staff for staff in staffs if staff.name == name), None)