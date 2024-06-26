import random
import datetime
from copy import deepcopy
from enum import Enum
from operator import attrgetter, itemgetter
# カレンダーの用意
cal_begin   = datetime.date(2024,7,1)
cal_end     = datetime.date(2024,9,30)
target_cal  = [cal_begin + datetime.timedelta(days = i) for i in range (0, (cal_end - cal_begin).days + 1)]
def is_weekday(date): # 週末＋祝日（2026年末分まで）を除外
    jpholidays = [
    datetime.date(2024, 1, 1), datetime.date(2024, 1, 8), datetime.date(2024, 2, 11), datetime.date(2024, 2, 12), datetime.date(2024, 3, 20), datetime.date(2024, 4, 29), datetime.date(2024, 5, 3), datetime.date(2024, 5, 4), datetime.date(2024, 5, 5), datetime.date(2024, 5, 6),
    datetime.date(2024, 7, 15), datetime.date(2024, 8, 11), datetime.date(2024, 8, 12), datetime.date(2024, 9, 16), datetime.date(2024, 9, 22), datetime.date(2024, 10, 14), datetime.date(2024, 11, 3), datetime.date(2024, 11, 4), datetime.date(2024, 11, 23), datetime.date(2024, 12, 23),
    datetime.date(2025, 1, 1), datetime.date(2025, 1, 13), datetime.date(2025, 2, 11), datetime.date(2025, 3, 20), datetime.date(2025, 4, 29), datetime.date(2025, 5, 3), datetime.date(2025, 5, 4), datetime.date(2025, 5, 5), datetime.date(2025, 5, 6),
    datetime.date(2025, 7, 21), datetime.date(2025, 8, 11), datetime.date(2025, 9, 15), datetime.date(2025, 9, 23), datetime.date(2025, 10, 13), datetime.date(2025, 11, 3), datetime.date(2025, 11, 23), datetime.date(2025, 11, 24), datetime.date(2025, 12, 23),
    datetime.date(2026, 1, 1), datetime.date(2026, 1, 12), datetime.date(2026, 2, 11), datetime.date(2026, 3, 20), datetime.date(2026, 4, 29), datetime.date(2026, 5, 3), datetime.date(2026, 5, 4), datetime.date(2026, 5, 5), datetime.date(2026, 5, 6),
    datetime.date(2026, 7, 20), datetime.date(2026, 8, 11), datetime.date(2026, 9, 21), datetime.date(2026, 9, 22), datetime.date(2026, 9, 23), datetime.date(2026, 10, 12), datetime.date(2026, 11, 3), datetime.date(2026, 11, 23), datetime.date(2026, 12, 23)
] 
    if date in jpholidays:
        return False
    else:
        return date.weekday() < 5
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
    Staff("山本",   rank=16,    ng_request =[datetime.date(2024,7,4),datetime.date(2024,8,24),]),
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
    Staff("谷本",   rank= 4,    ng_request =[date for date in target_cal if date.weekday() == 5]), #毎週金夜が外勤
    Staff("川上",   rank= 3,    ng_request =[datetime.date(2024,7,18),datetime.date(2024,7,19),]),
    Staff("河田",   rank= 3,    ng_request =[datetime.date(2024,7,1),datetime.date(2024,7,18),datetime.date(2024,7,19),datetime.date(2024,9,22),]),
    Staff("諏江",   rank= 3,    ng_request =[datetime.date(2024,7,1),datetime.date(2024,7,6),datetime.date(2024,7,18),datetime.date(2024,7,19),datetime.date(2024,8,24),datetime.date(2024,9,8),]),
    Staff("松山",   rank= 3,    ng_request =[datetime.date(2024,7,18),datetime.date(2024,7,19)]),
    Staff("野田",   rank= 3,    ng_request =[datetime.date(2024,7,13),]),
    Staff("瀧",     rank= 4,    ng_request =[datetime.date(2024,7,27),datetime.date(2024,8,10),datetime.date(2024,9,27),datetime.date(2024,9,28)]),
    # Staff("Kobayasi", rank= 3,    ng_request =[]),
    # Staff("Ikeda",    rank= 5,    ng_request =[]),
]
dummy_staff = Staff("Dummy", rank=10, certified_section = [Section.s30594, Section.s30595, Section.s30596], ng_request =[]),
def print_ng_count(staffs):
    ng_counts = {}
    print("PRINT TOO MUCH NGs on...")
    for date in target_cal:
        count = 0
        for staff in staffs:
            if date in staff.ng_request:
                count += 1
        if count > 4:
            print(f"{date}, ng={count}")
        # ng_counts[date] = count

def get_staff_by_name(name):
    return next((staff for staff in staffs if staff.name == name), None)
class Monthly_schedules:
    def __init__(self) -> None:
        self.schedules = {}
        for date in target_cal:
            daily_assigns = {
            Time.day    :{
                        Section.s30591: None,
                        Section.s30595: None,
                        Section.s30599: None,
                        Section.s30594: None,
                        Section.sEsub1: None,
                        Section.sEsub2: None,
                        Section.s30596: None,
                        Section.s30597: None,
                        Section.sIsub1: None,
                        Section.sIsub2: None,
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
            }}
            self.schedules[date] = daily_assigns
    def assign(self, date, time, section, name):
        staff = get_staff_by_name(name)
        time_category = Time.night if time == Time.night else Time.day
        check_isoff = (staff.personal_schedule[date][time_category] == Section.OFF)
        if not check_isoff:
            print(f"cannot assign {name} on {date},{time},{section}")
            return None
        if section == Section.extras:
            self.schedules[date][time][section].append(name)
        else:
            self.schedules[date][time][section] = name

        if time == Time.extra:
            if section == Section.taitou:
                staff.extra_count += 2
                staff.personal_schedule[date][Time.day] = section
                staff.personal_schedule[date][Time.night] = section                
            else:
                staff.extra_count += 1
                staff.personal_schedule[date][Time.day] = section            
        elif time == Time.day:
            staff.work_count += 1
            staff.personal_schedule[date][time] = section
        elif time == Time.night:
            staff.work_count += 1.5
            staff.personal_schedule[date][time] = section
    def assign_dummy(self, date, time, section):
        self.schedules[date][time][section] = "Dummy"
    def is_valid_assign(self, date) -> bool:
        staff_filled = all([self.schedules[date][Time.day][section] is not None for section in (Section.s30595, Section.s30599, Section.s30594, Section.s30596)] \
            + [self.schedules[date][Time.night][section] is not None for section in (Section.s30595, Section.s30599, Section.s30596)])
        
        day_staffs = [self.schedules[date][Time.day][section] for section in time_section[Time.day] if not None]
        night_staffs = [self.schedules[date][Time.night][section] for section in time_section[Time.night] if not None]
        extra_staffs = [self.schedules[date][Time.extra][section] for section in (Section.sonoda, Section.teikyo, Section.mitsui, Section.taitou, Section.oomori, Section.chibat) if not None]\
                    + self.schedules[date][Time.extra][Section.extras]
        day_staff_not_conflicted = True if len(day_staffs + extra_staffs) == len(set(day_staffs + extra_staffs)) else False
        night_staff_not_conflicted = True if len(night_staffs + extra_staffs) == len(set(night_staffs + extra_staffs)) else False
        return all([staff_filled, day_staff_not_conflicted, night_staff_not_conflicted]) # 必須セクションが埋まっていること、日勤＋外勤に重複がないこと、夜勤＋外勤に重複がないこと
    def assignable_stafflist(self, date, time):
        return [[staff.name, staff.work_count] for staff in staffs if staff.available(date, time)] if time in (Time.day, Time.night) else None
    def block_assignable_stafflist(self, date, min_blockdate):
        return [[staff.name, staff.available_days(date), staff.work_count] for staff in staffs if staff.available_days(date) >= min_blockdate]
    def assign_30591(self): # 30591を割り当て  山本：火水木30591、日曜夜30596 浅田：その他平日30591
        for date in target_cal:
            if is_weekday(date) and date.weekday() in (1, 2, 3):
                self.assign(date, Time.day, Section.s30591, "山本")
            elif is_weekday(date):
                self.assign(date, Time.day, Section.s30591, "浅田")
            elif date.weekday() == 6:
                self.assign(date, Time.night, Section.s30596, "山本")
    def assign_icu_and_eicu(self):
        icu_item = [
            {"main_section": Section.s30596, "sub_section": Section.s30597, "section_namelist": ["佐藤悠", "木村", "佐藤一"], "night_section": Section.s30596},
            {"main_section": Section.s30594, "sub_section": Section.sEsub1, "section_namelist": ["中野", "有田", "堂園", "池上"], "night_section": Section.s30595}
        ]
        for item in icu_item:
            main_section = item["main_section"]
            sub_section = item["sub_section"]
            section_namelist = item["section_namelist"]
            night_section = item["night_section"]
            for _ in range(30):
                print(f"\rASSIGN {"ICU" if main_section == Section.s30596 else "EICU"} {_+1}", end="") # デバッグ用
                new_monthly_schedules = deepcopy(self)
                saved_staff_states =  {staff.name: [deepcopy(staff.work_count), deepcopy(staff.personal_schedule)] for staff in staffs}
                check_date = cal_begin
                restart_flag = False
                previous_staff_name = None
                while check_date < cal_end:
                    if (cal_end - check_date).days <= 4:
                        block_assignable_stafflist = [[name, available_days, work_count] for name, available_days, work_count in self.block_assignable_stafflist(check_date, min_blockdate = (cal_end - check_date).days + 1) if name in section_namelist and name != previous_staff_name]
                    else: 
                        block_assignable_stafflist = [[name, available_days, work_count] for name, available_days, work_count in self.block_assignable_stafflist(check_date, min_blockdate = 5) if name in section_namelist and name != previous_staff_name]
                        if len(block_assignable_stafflist) == 0:
                            block_assignable_stafflist = [[name, available_days, work_count] for name, available_days, work_count in self.block_assignable_stafflist(check_date, min_blockdate = 4) if name in section_namelist and name != previous_staff_name]
                    if len(block_assignable_stafflist) == 0:
                        if previous_staff_name == "Dummy":
                            restart_flag = True
                            break
                        staff = dummy_staff
                        new_monthly_schedules.schedules[check_date][Time.day][sub_section] = "Dummy"
                        previous_staff_name = "Dummy"
                        check_date += datetime.timedelta(days = 1)
                        continue
                    sorted_stafflist = sorted(block_assignable_stafflist, key=itemgetter(2))[:3]
                    name, available_days, wc = random.choice(sorted_stafflist)
                    staff = get_staff_by_name(name)
                    assign_block = min(5, available_days)
                    if check_date + datetime.timedelta(days = assign_block) > cal_end:
                        assign_block = (cal_end - check_date).days + 1
                    for i in range(assign_block):
                        if i == 0:
                            if new_monthly_schedules.schedules[check_date][Time.day][main_section] is None:
                                new_monthly_schedules.assign(check_date, Time.day, main_section, name)
                            else:
                                new_monthly_schedules.assign(check_date, Time.day, sub_section, name)
                        else:
                            new_monthly_schedules.assign(check_date + datetime.timedelta(days = i), Time.day, main_section, name)
                        if i == assign_block - 1:
                            if new_monthly_schedules.schedules[check_date + datetime.timedelta(days = i)][Time.night][night_section] is None:
                                new_monthly_schedules.assign(check_date + datetime.timedelta(days = i), Time.night, night_section, name)
                    previous_staff_name = name
                    # staffはassign_block日分の勤務割り当てがあるが、main_section割り当て進行度は1日分少ないのでdatetime.timedelta(days = assign_block - 1)
                    check_date += datetime.timedelta(days = assign_block - 1)
                if restart_flag:
                    for staff in staffs:
                        staff.work_count, staff.personal_schedule = saved_staff_states[staff.name]
                    new_monthly_schedules = deepcopy(self)
                else:
                    self.schedules = new_monthly_schedules.schedules
                    print(f"...DONE")
                    break
            if restart_flag:
                print("...FAILED")
                return False
        return True
    def assign_nightshifts(self):
        section_namelists = {
            Section.s30595 : [staff.name for staff in staffs if Section.s30595 in staff.certified_section and not staff.is_phd],
            Section.s30596 : [staff.name for staff in staffs if Section.s30596 in staff.certified_section and not staff.is_phd],
            Section.s30599 : [staff.name for staff in staffs if staff.rank < 5]
        }
        help_namelists = {
            Section.s30595 : ["浅田", "高井", "水野", "佐藤拓", "田上"],
            Section.s30596 : ["浅田", "高井", "水野"],
            Section.s30599 : [staff.name for staff in staffs if staff.rank >= 5]
        }
        for _ in range(15):
            print(f"\rASSIGN NIGHT {_+1}", end="")
            saved_staff_states =  {staff.name: [deepcopy(staff.work_count), deepcopy(staff.personal_schedule)] for staff in staffs}
            new_monthly_schedules = deepcopy(self)
            restart_flag = False
            for section in (Section.s30596, Section.s30595, Section.s30599):    
                for date in target_cal:
                    # 既に割り振られてる場合はスキップ
                    if new_monthly_schedules.schedules[date][Time.night][section] is not None:
                        continue
                    # 祝日は院生優先
                    if not is_weekday(date) and section in (Section.s30596, Section.s30595):
                        primary_namelists = help_namelists[section]
                        secondary_namelist = section_namelists[section]
                    else:
                        primary_namelists = section_namelists[section]
                        secondary_namelist = help_namelists[section]
                    daily_names = [[name, work_count] for name, work_count in new_monthly_schedules.assignable_stafflist(date, Time.night) if name in primary_namelists]
                    if len(daily_names) == 0:
                        daily_names = [[name, work_count] for name, work_count in new_monthly_schedules.assignable_stafflist(date, Time.night) if name in secondary_namelist]
                        if len(daily_names) == 0:
                            restart_flag = True
                            break
                    min_count = sorted(daily_names, key=itemgetter(1))[0][1]
                    min_count_daily_names = [name for name, work_count in daily_names if work_count == min_count]
                    name = random.choice(min_count_daily_names)
                    new_monthly_schedules.assign(date, Time.night, section, name)
                if restart_flag:
                    break
            if restart_flag:
                for staff in staffs:
                    staff.work_count, staff.personal_schedule = saved_staff_states[staff.name]
            else:
                self.schedules = new_monthly_schedules.schedules
                print(f"...DONE")
                return True
        print("...FAILED")
        return False
    def assign_extra_shifts1(self):
        for _ in range(20):
            print(f"\rASSIGN EXTRA {_+1}", end="")
            saved_staff_states =  {staff.name: deepcopy(staff.personal_schedule) for staff in staffs}
            new_monthly_schedules = deepcopy(self)
            restart_flag = False
            for date in target_cal:
                # 台東(土日)、台東の月1縛りのため余計なギミックあり
                if date == date.replace(day=1):
                    monthly_taitou_box = ["河田", "川上", "野田", "松山", "諏江", "池上", "堂園", "佐藤一"]
                    monthly_taitou_help = ["木村", "有田", "中野", "佐藤悠"]
                if date.weekday() in (5, 6):
                    staff_namelist = [[staff.name, staff.extra_count] for staff in staffs if staff.name in monthly_taitou_box and staff.available_days(date) >= 1]
                    if len(staff_namelist) == 0:
                        staff_namelist = [[staff.name, staff.extra_count] for staff in staffs if staff.name in monthly_taitou_help and staff.available_days(date) >= 1]
                        if len(staff_namelist) == 0:
                            print(f"...FAILED {date} for 台東")
                            restart_flag = True
                            break
                    min_count = sorted(staff_namelist, key=itemgetter(1))[0][1]
                    staff_namelist = [name for name, work_count in staff_namelist if work_count == min_count]
                    name = random.choice(staff_namelist)
                    new_monthly_schedules.assign(date, Time.extra, Section.taitou, name)
                    monthly_taitou_box.remove(name) if name in monthly_taitou_box else monthly_taitou_help.remove(name)
            if restart_flag == True:
                for staff in staffs:
                    staff.extra_count = 0
                    staff.personal_schedule = saved_staff_states[staff.name]
                continue
            else:
                self.schedules = new_monthly_schedules.schedules
                print(f"...DONE")
                return True
        print(f"...FAILED")
        return False
    def assign_extra_shifts2(self):
        for _ in range(30):
            print(f"\rASSIGN EXTRA {_+1}", end="")
            saved_staff_states =  {staff.name: deepcopy(staff.personal_schedule) for staff in staffs}
            new_monthly_schedules = deepcopy(self)
            restart_flag = False
            for date in target_cal:
                # 千葉徳、大盛り、苑田、帝京はループ処理
                extra_item_list = [
                    ## 千葉徳（月、3-5年）に川田、川上、野田、松山、諏江、池上、堂園、佐藤一
                    {"hospital": Section.chibat, "weekday": (0,), "staffs": ("河田", "川上", "野田", "松山", "諏江", "池上", "堂園", "佐藤一")},
                    ## 大森（月火木、6-8年）に木村、有田、中野、佐藤悠、高井、佐藤拓
                    {"hospital": Section.oomori, "weekday": (0, 1, 3), "staffs": ("木村", "有田", "中野", "佐藤悠", "高井", "佐藤拓")},
                    ## 苑田（火木、3-4年）に川田、川上、野田、松山、諏江、池上
                    {"hospital": Section.sonoda, "weekday": (1, 3), "staffs": ("河田", "川上", "野田", "松山", "諏江", "池上")},
                    ## 帝京（月金、5-8年）に堂園、佐藤一、木村、有田、中野、佐藤悠
                    {"hospital": Section.teikyo, "weekday": (0, 4), "staffs": ("堂園", "佐藤一", "木村", "有田", "中野", "佐藤悠")}
                ]
                for item in extra_item_list:
                    if date.weekday() in item["weekday"]:
                        staff_namelist = [[staff.name, staff.extra_count] for staff in staffs if staff.name in item["staffs"] and staff.available(date, Time.day)]
                        if len(staff_namelist) > 0:
                            min_count = sorted(staff_namelist, key=itemgetter(1))[0][1]
                            staff_namelist = [name for name, work_count in staff_namelist if work_count == min_count]
                            name = random.choice(staff_namelist)
                            new_monthly_schedules.assign(date, Time.extra, item["hospital"], name)
                        else:
                            new_monthly_schedules.assign_dummy(date, Time.extra, item["hospital"])
                            '''print(f"...FAILED {date} for {item["hospital"]}") 
                            restart_flag = True
                            break'''
                if restart_flag:
                    break
                # 三井（水金）に水＝堀江、金＝山本、あと高井をランダム
                if date.weekday() in (2, 4):
                    namelist = ("山本", "堀江", "高井")
                    assigned_flag = False
                    for name in namelist:
                        staff = get_staff_by_name(name)
                        if staff.available(date, Time.day):
                            new_monthly_schedules.assign(date, Time.extra, Section.mitsui, staff.name)
                            assigned_flag = True
                            break
                        else:
                            continue
                    if not assigned_flag:
                        new_monthly_schedules.assign_dummy(date, Time.extra, Section.mitsui)
                        '''restart_flag = True
                        print(f"...FAILED {date} for 三井") 
                        break'''
            if restart_flag == True:
                for staff in staffs:
                    staff.extra_count = 0
                    staff.personal_schedule = saved_staff_states[staff.name]
                continue
            else:
                self.schedules = new_monthly_schedules.schedules
                print(f"...DONE")
                return True
        print(f"...FAILED")
        return False
    def assign_er(self, section):
        for _ in range(30):
            print(f"\rASSIGN ER {_+1}", end="")
            saved_staff_states =  {staff.name: [deepcopy(staff.work_count), deepcopy(staff.personal_schedule)] for staff in staffs}
            new_monthly_schedules = deepcopy(self)
            dummy_count = 0

            section_namelists = [staff.name for staff in staffs if staff.rank < 5] if section == Section.s30599 else [staff.name for staff in staffs if Section.s30595 in staff.certified_section and not staff.is_phd]
            for date in target_cal:
                daily_names = [[name, work_count] for name, work_count in new_monthly_schedules.assignable_stafflist(date, Time.day) if name in section_namelists]
                if len(daily_names) > 0:
                    min_count = sorted(daily_names, key=itemgetter(1))[0][1]
                    min_count_daily_names = [name for name, work_count in daily_names if work_count == min_count]
                    name = random.choice(min_count_daily_names)
                    new_monthly_schedules.assign(date, Time.day, section, name)
                else:
                    help_staffnames = [[name, work_count] for name, work_count in new_monthly_schedules.assignable_stafflist(date, Time.day) if name in ("浅田", "水野", "山本")]
                    if section == Section.s30595 and len(help_staffnames) > 0:
                        min_count = sorted(help_staffnames, key=itemgetter(1))[0][1]
                        min_count_daily_names = [name for name, work_count in help_staffnames if work_count == min_count]
                        name = random.choice(min_count_daily_names)
                        new_monthly_schedules.assign(date, Time.day, section, name)
                    else:
                        new_monthly_schedules.schedules[date][Time.day][section] = "Dummy"
                        dummy_count += 1
            if dummy_count > 5:
                for staff in staffs:
                    staff.work_count, staff.personal_schedule = saved_staff_states[staff.name]
                continue
            else:
                self.schedules = new_monthly_schedules.schedules
                print(f"...DONE")
                return True
        print(f"...FAILED")
        return False
    # def assign_sub_staffs(self):
    def swap(self, phd_staff, work_limit, time: Time):
        swap_count = 0
        time_count = 1 if time == Time.day else 1.5
        while work_limit >= phd_staff.work_count:
            assignable_date = [date for date in target_cal if phd_staff.available(date, time)]
            sections = [section for section in (Section.s30596, Section.s30595) if section in phd_staff.certified_section]
            # phd_staffが勤務可能な日、セクションの夜勤にすでに入っているスタッフとそのwork_countを拾う
            candidate_list = []
            for section in sections:
                for date in assignable_date:
                    swapping_name = self.schedules[date][time][section]
                    if swapping_name in ("Dummy", phd_staff.name) or swapping_name is None:
                        continue
                    swapping_staff = get_staff_by_name(swapping_name)
                    candidate_list.append([date, section, swapping_staff, swapping_staff.work_count])
            if len(candidate_list) == 0:
                section = Section.s30599
                for date in assignable_date:
                    swapping_name = self.schedules[date][time][section]
                    if swapping_name in ("Dummy", phd_staff.name) or swapping_name is None:
                        continue
                    swapping_staff = get_staff_by_name(swapping_name)
                    candidate_list.append([date, section, swapping_staff, swapping_staff.work_count])
                if len(candidate_list) == 0:
                    print("NONE SWAPPABLE")
                    break
            candidate_list = sorted(candidate_list, key=itemgetter(3), reverse=True)
            date, section, candidate, candidate_wc = candidate_list[0]
            # 勤務数最大の人から1回勤務をもらう
            candidate.work_count -= time_count
            candidate.personal_schedule[date][time] = Section.OFF
            self.assign(date, time, section, phd_staff.name)
            swap_count += 1
            print(f"\rswapped {phd_staff.name} {time} {swap_count} times...")
    def swap_phd(self):
        # 大学院2年目以降
        for name in ("高井", "佐藤拓", "田上"):
            print("SWAP PhD...")
            phd_staff = get_staff_by_name(name)
            work_limit = round((cal_end - cal_begin).days / 7) * 1.5
            self.swap(phd_staff, work_limit, Time.night)
            if work_limit > phd_staff.work_count:
                self.swap(phd_staff, work_limit, Time.day)
        # 大学院1年目
        name = "水野"
        phd_staff = get_staff_by_name(name)
        work_limit = round((cal_end - cal_begin).days / 7) * 1.5
        self.swap(phd_staff, work_limit, Time.night)
         # 日勤を週1程度増やすために嵩増し
        work_limit = round((cal_end - cal_begin).days / 7) * 2.5
        self.swap(phd_staff, work_limit, Time.day)

def main():
    print_ng_count(staffs)
    for i in range(50):
        print(f">>> RUNNING ATTEMPT {i+1}")
        for staff in staffs:
            staff.work_count = 0
            staff.extra_count = 0
            staff.personal_schedule = {date: {Time.day: Section.OFF, Time.night: Section.OFF} for date in target_cal}
            staff.personal_schedule.update({date: {Time.day: Section.NG, Time.night: Section.NG} for date in staff.ng_request})
        monthly_schedules = Monthly_schedules()
        monthly_schedules.assign_30591()
        flag = monthly_schedules.assign_icu_and_eicu()
        if not flag:
            continue
        flag = monthly_schedules.assign_nightshifts()
        if not flag:
            continue
        flag = monthly_schedules.assign_er(Section.s30595)
        if not flag:
            continue
        monthly_schedules.swap_phd()
        flag = monthly_schedules.assign_extra_shifts1()
        if not flag:
            continue
        flag = monthly_schedules.assign_extra_shifts2()
        if not flag:
            continue
        flag = monthly_schedules.assign_er(Section.s30599)
        if flag:
           break
    print("\n===============generated schedules===============")
    indexes = ["Date", "D_30591", "D_30595", "D_30599", "D_30594", "D_Esub1", "D_Esub2", "D_30596", "D_30597", "D_Isub1", "D_Isub2", "  | ", "N_30595", "N_30599", "N_30596", " || ", "苑田", "帝京", "三井", "大森", "台東", "千葉徳", "  | ", "個人外勤"]
    print("\t".join(indexes))
    for date, schedule in monthly_schedules.schedules.items():
        output = [f"{date.strftime('%m-%d')}"]
        for section in time_section[Time.day]:
            output.append(schedule[Time.day][section] if schedule[Time.day][section] else '  ')
        output.append("  | ")
        for section in time_section[Time.night]:
            output.append(schedule[Time.night][section] if schedule[Time.night][section] else '  ')
        output.append(" || ")
        output.append(schedule[Time.extra][Section.sonoda] if schedule[Time.extra][Section.sonoda] else ' ')
        output.append(schedule[Time.extra][Section.teikyo] if schedule[Time.extra][Section.teikyo] else ' ')
        output.append(schedule[Time.extra][Section.mitsui] if schedule[Time.extra][Section.mitsui] else ' ')
        output.append(schedule[Time.extra][Section.oomori] if schedule[Time.extra][Section.oomori] else ' ')
        output.append(schedule[Time.extra][Section.taitou] if schedule[Time.extra][Section.taitou] else ' ')
        output.append(schedule[Time.extra][Section.chibat] if schedule[Time.extra][Section.chibat] else ' ')
        output.append("  | ")
        #一旦個人外勤は置いとこう output.append(" ".join(schedule[Time.extra][Section.extras]) if schedule[Time.extra][Section.extras] else 'None')
        reset_color = '\033[0m'
        text_color = '\033[36m' if not is_weekday(date) else reset_color
        print(text_color + "\t".join(output) + reset_color) 

    print("===============staff work stats===============")
    for staff in staffs:
        actual_workcount = 0
        actual_extracount = 0
        for date in target_cal:
            for section in time_section[Time.day]:
                if monthly_schedules.schedules[date][Time.day][section] == staff.name:
                    actual_workcount += 1
            for section in time_section[Time.night]:
                if monthly_schedules.schedules[date][Time.night][section] == staff.name:
                    actual_workcount += 1.5
            for section in time_section[Time.extra]:
                if monthly_schedules.schedules[date][Time.extra][section] == staff.name:
                    actual_extracount += 2 if section == Section.taitou else 1
        print(f"{staff.name}", end="\t")
        print(f"works* {staff.work_count}({actual_workcount})", end="\t")
        print(f"extra_works* {staff.extra_count}({actual_extracount})")
main()