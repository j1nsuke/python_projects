import random
import datetime
from copy import deepcopy, copy
from enum import Enum
from operator import attrgetter

# カレンダーの用意
cal_begin   = datetime.date(2024,7,1)
cal_end     = datetime.date(2024,9,30)
target_cal  = [cal_begin + datetime.timedelta(days = i) for i in range (0, (cal_end - cal_begin).days + 1)]
def is_weekday(date):
    jpholidays = [
    datetime.date(2024, 1, 1),  # 元日
    datetime.date(2024, 1, 8),  # 成人の日
    datetime.date(2024, 2, 11),  # 建国記念の日
    datetime.date(2024, 2, 12),  # 建国記念の日 振替休日
    datetime.date(2024, 3, 20),  # 春分の日
    datetime.date(2024, 4, 29),  # 昭和の日
    datetime.date(2024, 5, 3),  # 憲法記念日
    datetime.date(2024, 5, 4),  # みどりの日
    datetime.date(2024, 5, 5),  # こどもの日
    datetime.date(2024, 5, 6),  # こどもの日 振替休日
    datetime.date(2024, 7, 15),  # 海の日
    datetime.date(2024, 8, 11),  # 山の日
    datetime.date(2024, 8, 12),  # 山の日 振替休日
    datetime.date(2024, 9, 16),  # 敬老の日
    datetime.date(2024, 9, 22),  # 秋分の日
    datetime.date(2024, 10, 14),  # 体育の日
    datetime.date(2024, 11, 3),  # 文化の日
    datetime.date(2024, 11, 4),  # 文化の日 振替休日
    datetime.date(2024, 11, 23),  # 勤労感謝の日
    datetime.date(2024, 12, 23),  # 天皇誕生日

    datetime.date(2025, 1, 1),  # 元日
    datetime.date(2025, 1, 13),  # 成人の日
    datetime.date(2025, 2, 11),  # 建国記念の日
    datetime.date(2025, 3, 20),  # 春分の日
    datetime.date(2025, 4, 29),  # 昭和の日
    datetime.date(2025, 5, 3),  # 憲法記念日
    datetime.date(2025, 5, 4),  # みどりの日
    datetime.date(2025, 5, 5),  # こどもの日
    datetime.date(2025, 5, 6),  # こどもの日 振替休日
    datetime.date(2025, 7, 21),  # 海の日
    datetime.date(2025, 8, 11),  # 山の日
    datetime.date(2025, 9, 15),  # 敬老の日
    datetime.date(2025, 9, 23),  # 秋分の日
    datetime.date(2025, 10, 13),  # 体育の日
    datetime.date(2025, 11, 3),  # 文化の日
    datetime.date(2025, 11, 23),  # 勤労感謝の日
    datetime.date(2025, 11, 24),  # 勤労感謝の日 振替休日
    datetime.date(2025, 12, 23),  # 天皇誕生日

    datetime.date(2026, 1, 1),  # 元日
    datetime.date(2026, 1, 12),  # 成人の日
    datetime.date(2026, 2, 11),  # 建国記念の日
    datetime.date(2026, 3, 20),  # 春分の日
    datetime.date(2026, 4, 29),  # 昭和の日
    datetime.date(2026, 5, 3),  # 憲法記念日
    datetime.date(2026, 5, 4),  # みどりの日
    datetime.date(2026, 5, 5),  # こどもの日
    datetime.date(2026, 5, 6),  # こどもの日 振替休日
    datetime.date(2026, 7, 20),  # 海の日
    datetime.date(2026, 8, 11),  # 山の日
    datetime.date(2026, 9, 21),  # 敬老の日
    datetime.date(2026, 9, 22),  # 国民の休日
    datetime.date(2026, 9, 23),  # 秋分の日
    datetime.date(2026, 10, 12),  # 体育の日
    datetime.date(2026, 11, 3),  # 文化の日
    datetime.date(2026, 11, 23),  # 勤労感謝の日
    datetime.date(2026, 12, 23),  # 天皇誕生日
    ]
    if date in jpholidays:
        return False
    else:
        return True if date.weekday() < 5 else False


class Time(Enum):
    day = "Day"
    night = "Night"
    extra = "Extra"
class Section(Enum):
    s30591 = "30591"
    s30595 = "30595"
    s30599 = "30599"
    s30596 = "30596"
    s30597 = "30597"
    sIfree = "Ifree"
    s30594 = '30594'
    sEfree = "Efree"

    OFF    = "OFF"
    NG     = "NG"

    sonoda = "Sonoda"
    teikyo = "Teikyo"
    mitsui = "Mitsui"
    oomori = "Oomori"
    taitou = "Taitou"
    chibat = "Chibatoku"
    extras = "Kojin_extras"
time_section = {
        Time.day: (Section.s30591, Section.s30595, Section.s30599, Section.s30594, Section.sEfree, Section.s30596, Section.s30597, Section.sIfree),
        Time.night: (Section.s30595, Section.s30599, Section.s30596),
        Time.extra: (Section.sonoda, Section.teikyo, Section.mitsui, Section.taitou, Section.oomori, Section.chibat, Section.extras)
}
class Personal_schedule():
    def __init__(self, ng_request: list):
        self.schedule = {}
        for date in target_cal:
            self.schedule[date] = {Time.day: Section.OFF, Time.night: Section.OFF}
        for date in ng_request:
            self.schedule[date][Time.day] = Section.NG
            self.schedule[date][Time.night] = Section.NG
    def available_days(self, date):
        count = 0
        check_date = date + datetime.timedelta(days = count)
        while self.schedule[check_date][Time.day] == Section.OFF and self.schedule[check_date][Time.night] == Section.OFF:
            count += 1
        return count
    def available_time(self, date, time:Time) -> bool:
        return True if self.schedule[date][time] == Section.OFF else False

class Staff():
    def __init__(self, name, rank, is_phd = False, assignable_section = None,  ng_request = None):
        self.name = name
        self.rank = rank
        self.assignable_section = assignable_section
        self.ng_request = ng_request if ng_request is not None else []
        self.is_phd = is_phd
        self.work_count = 0
        self.extra_work_count = 0
        self.personal_schedule = Personal_schedule(ng_request)

# スタッフ名簿
staffs = [
    Staff("Asada", rank=16,     assignable_section = [Section.s30591], ng_request =[]),
    Staff("Yamamoto", rank=16,  assignable_section = [Section.s30591], ng_request =[]),
    Staff("Wada", rank=18,      assignable_section = [Section.s30599, Section.sEfree, Section.s30595, Section.s30594], ng_request =[]),
    Staff("Horie", rank=17,     assignable_section = [Section.s30599, Section.sEfree, Section.s30595, Section.s30594], ng_request =[]),
    Staff("SatoTaku", rank=12,  assignable_section = [Section.s30599, Section.s30595, Section.s30594], ng_request =[], is_phd = True),
    Staff("Tagami", rank=12,    assignable_section = [Section.s30599, Section.s30595, Section.s30594], ng_request =[], is_phd = True),
    Staff("Takai", rank=10,     assignable_section = [Section.s30599, Section.s30595, Section.s30594, Section.s30596], ng_request =[], is_phd = True),
    Staff("Mizuno", rank=10,    assignable_section = [Section.s30599, Section.sIfree, Section.s30597, Section.sEfree, Section.s30595, Section.s30594, Section.s30596], ng_request =[], is_phd = True),
    Staff("SatoYuko", rank= 8,  assignable_section = [Section.s30599, Section.sIfree, Section.s30597, Section.s30595, Section.s30596], ng_request =[]),
    Staff("Nakano", rank= 6,    assignable_section = [Section.s30599, Section.sEfree, Section.s30595, Section.s30594], ng_request =[]),
    Staff("Kimura", rank= 6,    assignable_section = [Section.s30599, Section.sIfree, Section.s30597, Section.s30595, Section.s30596], ng_request =[]),
    Staff("Arita", rank= 6,     assignable_section = [Section.s30599, Section.sEfree, Section.s30595, Section.s30594], ng_request =[]),
    Staff("SatoKazu", rank= 5,  assignable_section = [Section.s30599, Section.sIfree, Section.s30597, Section.s30595, Section.s30596], ng_request =[]),
    Staff("Dozono", rank= 5,    assignable_section = [Section.s30599, Section.sIfree, Section.s30597, Section.s30595, Section.s30594, Section.s30596], ng_request =[]),
    Staff("Ikegami", rank= 4,   assignable_section = [Section.s30599, Section.sEfree, Section.s30594], ng_request =[]),
    Staff("Tanimoto", rank= 4,  assignable_section = [Section.s30599, Section.sEfree, Section.s30597, Section.sIfree], ng_request =[]),
    Staff("Kawakami", rank= 3,  assignable_section = [Section.s30599, Section.sEfree], ng_request =[]),
    Staff("Kawada", rank= 3,    assignable_section = [Section.s30599, Section.sEfree], ng_request =[]),
    Staff("Noda", rank= 3,      assignable_section = [Section.s30599, Section.sEfree], ng_request =[]),
    Staff("Matuyama", rank= 3,  assignable_section = [Section.s30599, Section.sEfree], ng_request =[]),
    Staff("Sue_", rank= 3,      assignable_section = [Section.s30599, Section.sEfree], ng_request =[]),
    Staff("Taki", rank= 7,      assignable_section = [Section.s30599, Section.sEfree, Section.sIfree, Section.s30597], ng_request =[]),
    # Staff("Kobayasi", rank= 3,    assignable_section = [Section.s30599, Section.sEfree], ng_request =[]),
    # Staff("Ikeda", rank= 5,    assignable_section = [Section.s30599, Section.sEfree], ng_request =[]),
]

class Daily_assigns:
    def __init__(self, date:datetime.date) -> None:
        self.date = date
        self.staff_of = {
            Time.day    :{
                        Section.s30591: None,
                        Section.s30595: None,
                        Section.s30599: None,
                        Section.s30596: None,
                        Section.s30597: None,
                        Section.sIfree: [],
                        Section.s30594: None,
                        Section.sEfree: []
            },
            Time.night  :{
                        Section.s30595: None,
                        Section.s30599: None,
                        Section.s30596: None
            },
            Time.extra  :{
                        Section.sonoda: None,
                        Section.teikyo: None,
                        Section.mitsui: None,
                        Section.oomori: None,
                        Section.taitou: None,
                        Section.chibat: None,
                        Section.extras: []
            }
        }
    def assign(self, time, section, staff: Staff):
        if section in (Section.sEfree, Section.sIfree, Section.extras):
            self.staff_of[time][section].append(staff.name)
        else:
            self.staff_of[time][section] = staff.name

        if time == Time.extra:
            if section == Section.taitou:
                staff.extra_work_count += 2
                staff.personal_schedule[self.date][Time.day] = section
                staff.personal_schedule[self.date][Time.night] = section                
            else:
                staff.extra_work_count += 1
                staff.personal_schedule[self.date][Time.day] = section            
        elif time == Time.day:
            staff.work_count += 1
            staff.personal_schedule[self.date][time] = section
        elif time == Time.night:
            staff.work_count += 1.5
            staff.personal_schedule[self.date][time] = section
    def is_valid(self) -> bool:
        staff_filled = all([self.staff_of[Time.day][section] is not None for section in (Section.s30595, Section.s30599, Section.s30594, Section.s30596)] \
            + [self.staff_of[Time.night][section] is not None for section in (Section.s30595, Section.s30599, Section.s30596)])
        
        day_staffs = [self.staff_of[Time.day][section] for section in (Section.s30591, Section.s30595, Section.s30599, Section.s30594, Section.s30596, Section.s30597) if not None]\
                    + self.staff_of[Time.day][Section.sIfree] + self.staff_of[Time.day][Section.sEfree]
        night_staffs = [self.staff_of[Time.night][section] for section in (Section.s30595, Section.s30599, Section.s30596) if not None]
        extra_staffs = [self.staff_of[Time.extra][section] for section in (Section.sonoda, Section.teikyo, Section.mitsui, Section.taitou, Section.oomori, Section.chibat) if not None]\
                    + self.staff_of[Time.extra][Section.extras]
        day_staff_not_conflicted = True if len(day_staffs + extra_staffs) == len(set(day_staffs + extra_staffs)) else False
        night_staff_not_conflicted = True if len(night_staffs + extra_staffs) == len(set(night_staffs + extra_staffs)) else False
        return all([staff_filled, day_staff_not_conflicted, night_staff_not_conflicted]) # 必須セクションが埋まっていること、日勤＋外勤に重複がないこと、夜勤＋外勤に重複がないこと
    
class Monthly_assigns:
    def __init__(self) -> None:
        self.schedules = {}
        for date in target_cal:
            daily_assigns = Daily_assigns(date)
            self.schedules[date] = daily_assigns

    def daily_assignable_staffs(self, date, include_phd = False):
        # 勤務不可日とその前日夜勤を除外して勤務可能者リストを作成、院生を除外
        next_date = date + datetime.timedelta(days = 1)
        if include_phd == False:
            day_assignable = [staff for staff in staffs if not staff.is_phd and date not in staff.ng_request]
        else:
            day_assignable = [staff for staff in staffs if date not in staff.ng_request]
        night_assignable = [staff for staff in day_assignable if next_date not in staff.ng_request]
        # 前日夜勤者を除外リストに taitouを追加！
        previous_night_staffs = []
        if date != cal_begin:
            previous_day = date - datetime.timedelta(days = 1)
            previous_day_schedule = self.schedules[previous_day]
            previous_night_staffs = [previous_day_schedule.staff_of[Time.night][section] for section in night_sections if previous_day_schedule.staff_of[Time.night][section]]
            previous_night_staffs.append(previous_day_schedule.staff_of[Time.extra][Section.taitou] if previous_day_schedule.staff_of[Time.extra][Section.taitou] is not None else None)
        # 当日勤務者を除外リストに
        same_date_day_staffs = []
        same_date_schedule = self.schedules[date]
        for time in (Time.day, Time.extra):
            for section in self.schedules[date].staff_of[time]:
                if same_date_schedule.staff_of[time][section] is not None:
                    if section in (Section.sEfree, Section.sIfree, Section.extras):
                        same_date_day_staffs += same_date_schedule.staff_of[time][section]
                    else:
                        same_date_day_staffs.append(same_date_schedule.staff_of[time][section])
        same_date_night_staffs = [same_date_schedule.staff_of[Time.night][section] for section in night_sections if same_date_schedule.staff_of[Time.night][section] is not None]
        # 翌日勤務者を夜勤の除外リストに
        next_date_all_staffs = []
        if next_date <= cal_end:
            next_date_schedule = self.schedules[next_date]
            for time in Time:
                for section in self.schedules[next_date].staff_of[time]:
                    if next_date_schedule.staff_of[time][section] is not None:
                        if section in (Section.sEfree, Section.sIfree, Section.extras):
                            next_date_all_staffs += next_date_schedule.staff_of[time][section]
                        else:
                            next_date_all_staffs.append(next_date_schedule.staff_of[time][section])
        # 除外リストを使用
        day_assignable = [staff for staff in day_assignable if staff not in previous_night_staffs + same_date_day_staffs]
        night_assignable = [staff for staff in night_assignable if staff not in previous_night_staffs + same_date_night_staffs+ next_date_all_staffs]
        return [day_assignable, night_assignable]
    def copy_matrix(self): # copyの際にmatrix内のスタッフインスタンスが新生されて参照ズレが起こるのを修正
        temp_matrix = deepcopy(self)
        for date in temp_matrix.calendar:
            for time in Time:
                for section in temp_matrix.schedules[date].staff_of[time]:
                    if temp_matrix.schedules[date].staff_of[time][section] is not None:
                        temp_staff = temp_matrix.schedules[date].staff_of[time][section]
                        if section in (Section.sEfree, Section.sIfree, Section.extras):
                            real_staff = [get_staff_by_name(staff.name) for staff in temp_staff]
                            temp_matrix.schedules[date].staff_of[time][section] = real_staff
                        else:
                            real_staff = get_staff_by_name(temp_staff.name)
                            temp_matrix.schedules[date].staff_of[time][section] = real_staff
        return temp_matrix