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
    def assignable_staffs(self, date, time): #[Staff, Staff, ...]
        return [staff for staff in staffs if staff.available(date, time)] if time in (Time.day, Time.night) else None
    def block_assignable_stafflist(self, date, min_blockdate): #[[name, available_days, workcount], ...]
        return [[staff.name, staff.available_days(date), staff.work_count] for staff in staffs if staff.available_days(date) >= min_blockdate]
    ##################################################################################################
    def assign_30591(self): # 30591を割り当て  山本：火水木30591、日曜夜30596 浅田：その他平日30591
        for date in target_cal:
            if is_weekday(date) and date.weekday() in (1, 2, 3):
                self.assign(date, Time.day, Section.s30591, "山本")
            elif is_weekday(date):
                self.assign(date, Time.day, Section.s30591, "浅田")
            elif date.weekday() == 6:
                self.assign(date, Time.night, Section.s30596, "山本")
    def assign_taitou(self):
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
    def assign_icu_and_eicu(self): # 30594, Esub, 30596, 30597を3-5日ブロックで割り当て
        icu_itemsets = [
            {"main_staffs": ["佐藤悠", "木村", "佐藤一"],       "help_staffs":["中野", "堂園", "浅田"], "main_section": Section.s30596, "sub_section": Section.s30597, "night_section": Section.s30596},
            {"main_staffs": ["中野", "有田", "堂園", "池上"],   "help_staffs":["堀江", "和田", "水野"], "main_section": Section.s30594, "sub_section": Section.sEsub1, "night_section": Section.s30595}
        ]
        for item in icu_itemsets:
            main_section = item["main_section"]
            sub_section = item["sub_section"]
            main_staffs = item["main_staffs"]
            night_section = item["night_section"]
            help_staffs = item["help_staffs"]
            for _ in range(100):
                print(f"\rASSIGN {"ICU" if main_section == Section.s30596 else "EICU"} {_+1}", end="")
                new_monthly_schedules = deepcopy(self)
                saved_staff_states =  {staff.name: [deepcopy(staff.work_count), deepcopy(staff.personal_schedule)] for staff in staffs}
                check_date = cal_begin
                dummy_flag = False
                restart_flag = False
                previous_staff_name = None
                while cal_end > check_date:
                    block_assignable_stafflist = [[name, available_days, work_count] for name, available_days, work_count in self.block_assignable_stafflist(check_date, min_blockdate = 1) if name in main_staffs and name != previous_staff_name]
                    block_num = random.choice([4,4,5,5,5,5,5]) if (cal_end - check_date).days > 4 else (cal_end - check_date).days + 1 # 単なる重み付けrandom、最終日近辺はブロック端数調整
                    block_num_stafflist = [staff for staff in block_assignable_stafflist if staff[1] >= block_num]
                    if len(block_num_stafflist) == 0: #main_staffsを割振れない場合。previous_staffは変えないように変更。
                        if dummy_flag: #1回目はスルー、2回目は下のフラグ立ってるから分岐
                            helpers = [staff for staff in new_monthly_schedules.assignable_staffs(check_date, Time.day) if staff.name in help_staffs]
                            if len(helpers) == 0:
                                print(f"\rASSIGN {"ICU" if main_section == Section.s30596 else "EICU"} {_+1} ...FAILED ON {check_date}", end="")
                                restart_flag = True
                                break
                                #dummyに逃げるメソッドもある
                                '''new_monthly_schedules.assign_dummy(check_date, Time.day, main_section) 
                                check_date += datetime.timedelta(days= 1)
                                continue'''
                            else:
                                helper = random.choice(helpers)
                                new_monthly_schedules.assign(check_date, Time.day, main_section, helper.name) #help_staffsがいればそれをassign。ただしフラグは戻さない。
                                # previous_staff_name = helper.name
                                check_date += datetime.timedelta(days= 1)
                                continue
                        dummy_flag = True
                        # previous_staff_name = None
                        check_date += datetime.timedelta(days= 1)
                        continue
                    block_num_stafflist = sorted(block_num_stafflist, key = itemgetter(2))
                    min_work_count = block_num_stafflist[0][2]
                    block_num_stafflist = [staff for staff in block_num_stafflist if staff[2] == min_work_count]
                    name, available_days, wc = random.choice(block_num_stafflist)
                    staff = get_staff_by_name(name)
                    for i in range(block_num):
                        if i == 0:
                            if new_monthly_schedules.schedules[check_date][Time.day][main_section] is None:
                                new_monthly_schedules.assign(check_date, Time.day, main_section, name)
                            else:
                                new_monthly_schedules.assign(check_date, Time.day, sub_section, name)
                        else:
                            new_monthly_schedules.assign(check_date + datetime.timedelta(days = i), Time.day, main_section, name)
                        if i == block_num - 1:
                            if new_monthly_schedules.schedules[check_date + datetime.timedelta(days = i)][Time.night][night_section] is None:
                                if name == "池上":
                                    new_monthly_schedules.assign(check_date + datetime.timedelta(days = i), Time.night, Section.s30599, name)
                                else:   
                                    new_monthly_schedules.assign(check_date + datetime.timedelta(days = i), Time.night, night_section, name)
                    previous_staff_name = name
                    dummy_flag = False # dummyつかっていたらここで解除
                    check_date += datetime.timedelta(days = block_num - 1)
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
    def assign_day_night(self): # 30595, 30599, 夜勤, 外勤を日ごとに割り当て
        for date in target_cal:
            # 外勤→夜勤→日勤
            extra_list = []
            if is_weekday(date):
                daily_day_staffs = self.assignable_staffs(date, Time.day) # [Staff,...]
                extra_list = self.find_GAIKIN(date, daily_day_staffs) # [[section, name],...]
            for section, name in extra_list:
                self.assign(date, Time.extra, section, name) if name != "Dummy" else self.assign_dummy(date, Time.extra, section)

            night_list = []
            daily_night_staffs = [staff for staff in self.assignable_staffs(date, Time.night) if staff.name not in [sec_name[1] for sec_name in extra_list]]
            night_list = self.find_nightstaffs(date, daily_night_staffs) # None or [[section, name],...]
            for section, name in night_list:
                if self.schedules[date][Time.night][section] is None: # 夜勤は割当て済みの場合あり
                    self.assign(date, Time.night, section, name) if name != "Dummy" else self.assign_dummy(date, Time.night, section)

            er_list = []
            daily_day_staffs = [staff for staff in self.assignable_staffs(date, Time.day) if staff.name not in [sec_name[1] for sec_name in extra_list]] # [Staff,...]
            er_list = self.find_erstaffs(date, daily_day_staffs) # [[section, name],...]

            for section, name in er_list:
                self.assign(date, Time.day, section, name) if name != "Dummy" else self.assign_dummy(date, Time.day, section)
    def find_nightstaffs(self, date, daily_night_staffs):
        main_staffs = {
            Section.s30596 : [staff.name for staff in staffs if Section.s30596 in staff.certified_section and not staff.is_phd],
            Section.s30595 : [staff.name for staff in staffs if Section.s30595 in staff.certified_section and not staff.is_phd],
            Section.s30599 : [staff.name for staff in staffs if staff.rank < 5]
        }
        help_namelists = {
            Section.s30596 : [staff.name for staff in staffs if Section.s30596 in staff.certified_section and staff.is_phd] + ["浅田", ],
            Section.s30595 : [staff.name for staff in staffs if Section.s30595 in staff.certified_section and staff.is_phd] + ["浅田", ],
            Section.s30599 : [staff.name for staff in staffs if staff.rank >= 5]
        }
        night_list = []
        restart_flag = False
        for section in (Section.s30596, Section.s30595, Section.s30599):
            # 既に割り振られてる場合はスキップ
            if self.schedules[date][Time.night][section] is not None:
                continue
            # 祝日は院生優先
            if not is_weekday(date) and section in (Section.s30596, Section.s30595):
                primary_namelist = help_namelists[section]
                secondary_namelist = main_staffs[section]
            else:
                primary_namelist = main_staffs[section]
                secondary_namelist = help_namelists[section]
            staff_list = [[staff.name, staff.work_count] for staff in daily_night_staffs if staff.name in primary_namelist]
            if len(staff_list) == 0:
                staff_list = [[staff.name, staff.work_count] for staff in daily_night_staffs if staff.name in secondary_namelist]
                if len(staff_list) == 0:
                    night_list.append([section, "Dummy"])
                    continue
                    '''restart_flag = True
                    break'''
            min_count = sorted(staff_list, key=itemgetter(1))[0][1]
            min_count_staff_list = [name for name, work_count in staff_list if work_count == min_count]
            candidate_name = random.choice(min_count_staff_list)
            candidate = get_staff_by_name(candidate_name)
            night_list.append([section, candidate_name])
            daily_night_staffs.remove(candidate)
        if restart_flag:
            return False
        else:
            return night_list
    def find_GAIKIN(self, date, daily_day_staffs):
        extra_item_list = [
            ## 千葉徳（月、3-5年）に川田、川上、野田、松山、諏江、池上、堂園、佐藤一
            {"hospital": Section.chibat, "weekday": (0,), "staffs": ("河田", "川上", "野田", "松山", "諏江", "池上", "堂園", "佐藤一")},
            ## 大森（月火木、6-8年）に木村、有田、中野、佐藤悠、高井、佐藤拓
            {"hospital": Section.oomori, "weekday": (0, 1, 3), "staffs": ("木村", "有田", "中野", "佐藤悠", "高井", "佐藤拓")},
            ## 苑田（火木、3-4年）に川田、川上、野田、松山、諏江、池上
            {"hospital": Section.sonoda, "weekday": (1, 3), "staffs": ("河田", "川上", "野田", "松山", "諏江", "池上")},
            ## 帝京（月金、5-8年）に堂園、佐藤一、木村、有田、中野、佐藤悠
            {"hospital": Section.teikyo, "weekday": (0, 4), "staffs": ("堂園", "佐藤一", "木村", "有田", "中野", "佐藤悠")},
            ## 三井（水金）に山本、堀江、高井
            {"hospital": Section.mitsui, "weekday": (2, 4), "staffs": ("山本", "堀江", "高井")}
        ]
        extra_list = []
        for item in extra_item_list:
            if date.weekday() in item["weekday"]:
                staff_namelist = [[staff.name, staff.extra_count] for staff in daily_day_staffs if staff.name in item["staffs"]]
                if len(staff_namelist) > 0:
                    min_count = sorted(staff_namelist, key=itemgetter(1))[0][1]
                    staff_namelist = [name for name, work_count in staff_namelist if work_count == min_count]
                    name = random.choice(staff_namelist)
                    staff = get_staff_by_name(name)
                    extra_list.append([item["hospital"], name])
                    daily_day_staffs.remove(staff)
                else:
                    extra_list.append([item["hospital"], "Dummy"])
        return extra_list
    def find_erstaffs(self, date, daily_day_staffs):
        s30599_namelist = [[staff.name, staff.work_count] for staff in daily_day_staffs if staff.rank < 5]
        er_list = []
        if len(s30599_namelist) == 0:
            er_list.append([Section.s30599, "Dummy"])
        else:
            min_work_count = sorted(s30599_namelist, key=itemgetter(1))[0][1]
            s30599_namelist = [name for name, work_count in s30599_namelist if work_count == min_work_count]
            name = random.choice(s30599_namelist)
            er_list.append([Section.s30599, name])
        
        s30595_namelist = [[staff.name, staff.work_count] for staff in daily_day_staffs if Section.s30595 in staff.certified_section and not staff.is_phd]
        if len(s30595_namelist) == 0:
            er_list.append([Section.s30595, "Dummy"])
        else:
            min_work_count = sorted(s30595_namelist, key=itemgetter(1))[0][1]
            s30595_namelist = [name for name, work_count in s30595_namelist if work_count == min_work_count]
            name = random.choice(s30595_namelist)
            er_list.append([Section.s30595, name])
        return er_list        
    def find_free_candidates(self):
        freestaffs = [staff for staff in staffs if staff.rank < 5]
        for staff in freestaffs:
            print(f"{staff.name}: ", end='\t')
            date = cal_begin
            unoccupied_cal = []
            while cal_end >= date: #[[開始日, 連続勤務可能数], ...]
                workable_days = staff.available_days(date)
                if workable_days == 0:
                    date += datetime.timedelta(days = 1)
                else:
                    unoccupied_cal.append([date, workable_days])
                    if workable_days >= 3:
                        print(f"{date} -> {workable_days} 連勤可能", end='\t')
                    date += datetime.timedelta(days = workable_days)
            print('')

    ##################################################################################################
    def swap_GAIKIN_dummy(self):
        extra_item_list = {
            Section.chibat: ("河田", "川上", "野田", "松山", "諏江", "池上", "堂園", "佐藤一"),
            Section.oomori: ("木村", "有田", "中野", "佐藤悠", "高井", "佐藤拓"),
            Section.sonoda: ("河田", "川上", "野田", "松山", "諏江", "池上"),
            Section.teikyo: ("堂園", "佐藤一", "木村", "有田", "中野", "佐藤悠"),
            Section.mitsui: ("山本", "堀江", "高井"),
        }
        for date in target_cal:
            for section in time_section[Time.extra]:
                if self.schedules[date][Time.extra][section] == "Dummy":
                    stafflist = extra_item_list[section]
                    day_staffnames = [self.schedules[date][Time.day][section] for section in time_section[Time.day]]
                    night_staffnames = [self.schedules[date][Time.night][section] for section in time_section[Time.night]]
                    if date != cal_begin:
                        previous_night_staffnames = [self.schedules[date - datetime.timedelta(days = 1)][Time.night][section] for section in time_section[Time.night]]
                    swappable_staffnames = [name for name in stafflist if name in day_staffnames and name not in night_staffnames + previous_night_staffnames]
                    if len(swappable_staffnames) == 0:
                        print(f"DUMMY SWAP {date.strftime('%m-%d')}: NONE SWAPPABLE")
                    else:
                        swap_staffname = random.choice(swappable_staffnames) # 交代できる人をみつけたら、personal_scheduleをOFFにしてwork_countも減らしてから割当て
                        swap_staff = get_staff_by_name(swap_staffname)
                        erased_section = swap_staff.personal_schedule[date][Time.day]
                        print(f"DUMMY SWAP {date.strftime('%m-%d')}: {swap_staffname} {erased_section} -> {section} AND ", end="")
                        swap_staff.personal_schedule[date][Time.day] = Section.OFF
                        swap_staff.work_count -= 1
                        self.assign(date, Time.extra, section, swap_staffname)
                        self.assign_dummy(date, Time.day, erased_section)


                        if erased_section in (Section.sEsub1, Section.s30597, Section.s30591):
                            print(f"DONE")
                        elif erased_section in (Section.s30594, Section.s30595, Section.s30596):
                            replaceable_staffs = [staff for staff in self.assignable_staffs(date, Time.day) if erased_section in staff.certified_section]
                            if len(replaceable_staffs) == 0:
                                print(f"CANNOT FILL {erased_section}")
                            else:
                                replace_staff = random.choice(replaceable_staffs)
                                self.assign(date, Time.day, erased_section, replace_staff.name)
                                print(f"{replace_staff.name} OFF -> {erased_section}")
                        elif erased_section == Section.s30599:
                            replaceable_staffs = [staff for staff in self.assignable_staffs(date, Time.day) if staff.rank < 5]
                            if len(replaceable_staffs) == 0:
                                replaceable_staffs = [staff for staff in self.assignable_staffs(date, Time.day) if staff.rank >= 5]
                                if len(replaceable_staffs) == 0:
                                    print(f"CANNOT FILL {erased_section}")
                            replace_staff = random.choice(replaceable_staffs)
                            self.assign(date, Time.day, erased_section, replace_staff.name)
                            print(f"{replace_staff.name} Section.OFF -> {erased_section}")
    def swap(self, phd_staff, work_limit, time: Time):
        while work_limit >= phd_staff.work_count:
            time_count = 1 if time == Time.day else 1.5
            sections = [Section.s30595, Section.s30594] if time == Time.day else [section for section in (Section.s30596, Section.s30595) if section in phd_staff.certified_section]
            assignable_date = [date for date in target_cal if phd_staff.available(date, time)]
            # phd_staffが勤務可能な日、セクションの夜勤にすでに入っているスタッフとそのwork_countを拾う
            candidate_list = []
            for section in sections:
                for date in assignable_date:
                    swapping_name = self.schedules[date][time][section]
                    if swapping_name in ("Dummy", phd_staff.name, "山本") or swapping_name is None:
                        continue
                    swapping_staff = get_staff_by_name(swapping_name)
                    candidate_list.append([date, section, swapping_staff, swapping_staff.work_count])
            # 勤務枠余ってるのに入れるところがなければ30599も替わる（主に台東の条件緩めるため）
            if len(candidate_list) == 0:
                section = Section.s30599
                for date in assignable_date:
                    swapping_name = self.schedules[date][time][section]
                    if swapping_name in ("Dummy", phd_staff.name) or swapping_name is None:
                        continue
                    swapping_staff = get_staff_by_name(swapping_name)
                    candidate_list.append([date, section, swapping_staff, swapping_staff.work_count])
                if len(candidate_list) == 0:
                    print("NO MORE SWAPPABLE")
                    break
            candidate_list = sorted(candidate_list, key=itemgetter(3), reverse=True)
            date, section, candidate, candidate_wc = candidate_list[0]
            # 勤務数最大の人から1回勤務をもらう
            candidate.work_count -= time_count
            candidate.personal_schedule[date][time] = Section.OFF
            self.assign(date, time, section, phd_staff.name)
            print(f"PhD SWAP {date.strftime('%m-%d')} {time}: {section} {candidate.name} -> {phd_staff.name}")
    def swap_phd(self):
        # 大学院2年目以降
        for name in ("高井", "佐藤拓", "田上"):
            phd_staff = get_staff_by_name(name)
            work_limit = round((cal_end - cal_begin).days / 7) * 1.5
            self.swap(phd_staff, work_limit, Time.night)
            if work_limit > phd_staff.work_count:
                self.swap(phd_staff, work_limit, Time.day)
        # 大学院1年目
        for name in ("水野",):
            phd_staff = get_staff_by_name(name)
            work_limit = round((cal_end - cal_begin).days / 7) * 1.5
            self.swap(phd_staff, work_limit, Time.night)
            # 日勤を週1程度増やすために嵩増し
            work_limit = round((cal_end - cal_begin).days / 7) * 2.5
            self.swap(phd_staff, work_limit, Time.day)
    def swap_DAY_NIGHT_dummy(self):
        for date in target_cal:
            for time in (Time.night, Time.day):
                for section in time_section[time]:
                    if self.schedules[date][time][section] == "Dummy":
                        print(f"DUMMY FOUND {date.strftime('%m-%d')} {time}...{section} ", end="")
                        if section in (Section.sEsub1, Section.s30597, Section.s30591):
                            self.schedules[date][time][section] = None
                            print("ERACED")
                        elif section in (Section.s30594, Section.s30595, Section.s30596):
                            asada = get_staff_by_name("浅田")
                            help_asada = [asada, ] if asada.available(date, time) else []
                            replaceable_staffs = [staff for staff in self.assignable_staffs(date, time) if section in staff.certified_section] + help_asada
                            if len(replaceable_staffs) == 0:
                                print("CANNOT FILL")
                            else:
                                replace_staff = random.choice(replaceable_staffs)
                                self.assign(date, time, section, replace_staff.name)
                                print(f"FILLED by {replace_staff.name}")
                        elif section == Section.s30599:
                            replaceable_staffs = [staff for staff in self.assignable_staffs(date, time) if staff.rank < 5]
                            if len(replaceable_staffs) == 0:
                                replaceable_staffs = [staff for staff in self.assignable_staffs(date, time) if staff.rank >= 5]
                                if len(replaceable_staffs) == 0:
                                    print(f"CANNOT FILL")
                            replace_staff = random.choice(replaceable_staffs)
                            self.assign(date, time, section, replace_staff.name)
                            print(f"FILLED by {replace_staff.name}")

    def print_generated_schedules(self):
        print("\n===============generated schedules===============")
        indexes = ["Date", "D_30591", "D_30595", "D_30599", "D_30594", "D_Esub1", "D_Esub2", "D_30596", "D_30597", "D_Isub1", "D_Isub2", "  | ", "N_30595", "N_30599", "N_30596", " || ", "苑田", "帝京", "三井", "大森", "台東", "千葉徳", "  | ", "個人外勤"]
        print("\t".join(indexes))
        for date, schedule in self.schedules.items():
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
            reset_color = '\033[0m'
            text_color = '\033[36m' if not is_weekday(date) else reset_color
            print(text_color + "\t".join(output) + reset_color) 
    def print_staff_stats(self):
        print("===============staff work stats===============")
        print("名前\t\t計算\t(別計算の整合チェック)\t\t\t計算\t(別計算の整合チェック)")
        for staff in staffs:
            actual_daycount = 0
            actual_nightcount = 0
            actual_extracount = 0
            for date in target_cal:
                for section in time_section[Time.day]:
                    if self.schedules[date][Time.day][section] == staff.name:
                        actual_daycount += 1
                for section in time_section[Time.night]:
                    if self.schedules[date][Time.night][section] == staff.name:
                        actual_nightcount += 1
                for section in time_section[Time.extra]:
                    if self.schedules[date][Time.extra][section] == staff.name:
                        actual_extracount += 2 if section == Section.taitou else 1
            print(f"{staff.name}\tコマ数: {staff.work_count}\t({actual_daycount + actual_nightcount * 1.5} = DAY:{actual_daycount} + NIGHT:{actual_nightcount})\t外勤数: {staff.extra_count}\t({actual_extracount})")
    
    print("===============staff personal calendar===============")
    '''
    for staff in staffs:
        personal_cal = []
        for date in target_cal:
            if staff.personal_schedule[date][Time.day] == Section.NG:
                daily = "××"
            else:
                daily = "□" if staff.personal_schedule[date][Time.day] == Section.OFF else "■"
                daily += "□" if staff.personal_schedule[date][Time.night] == Section.OFF else "■"
            personal_cal.append(daily)
        print(f"{staff.name}: " + ' '.join(personal_cal))
    '''
    index = ["Date", ] + [staff.name for staff in staffs]
    print('\t'.join(index))
    for date in target_cal:
        cals = []
        for staff in staffs:
            if staff.personal_schedule[date][Time.day] == Section.NG:
                daily = "××"
            else:
                daily = "_" if staff.personal_schedule[date][Time.day] == Section.OFF else "■"
                daily += "_" if staff.personal_schedule[date][Time.night] == Section.OFF else "■"
            cals.append(daily)
        reset_color = '\033[0m'
        text_color = '\033[36m' if not is_weekday(date) else reset_color
        print(text_color + f"{date.strftime('%m-%d')}", end='\t')
        print('\t'.join(cals) + reset_color)
        
        

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
        flag = monthly_schedules.assign_taitou()
        if not flag:
            continue
        flag = monthly_schedules.assign_icu_and_eicu()
        if not flag:
            continue
        monthly_schedules.assign_day_night()
        monthly_schedules.swap_GAIKIN_dummy()
        monthly_schedules.swap_phd()
        monthly_schedules.swap_DAY_NIGHT_dummy()
        break
    
    print_generated_schedules(monthly_schedules)
    print_staff_stats(monthly_schedules)
    monthly_schedules.find_free_candidates()

    
main()