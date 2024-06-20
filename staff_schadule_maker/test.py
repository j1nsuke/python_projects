import random
import datetime
from copy import deepcopy
from enum import Enum
from operator import attrgetter, itemgetter
# カレンダーの用意
cal_begin   = datetime.date(2024,7,1)
cal_end     = datetime.date(2024,7,30)
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
    sIfree = "Ifree"
    s30594 = '30594'
    sEfree = "Efree"

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
        Time.day: (Section.s30591, Section.s30595, Section.s30599, Section.s30594, Section.sEfree, Section.s30596, Section.s30597, Section.sIfree),
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
        self.extra_work_count = 0
        self.personal_schedule = {}
        for date in target_cal:
            self.personal_schedule[date] = {Time.day: Section.OFF, Time.night: Section.OFF}
        for date in ng_request:
            self.personal_schedule[date][Time.day] = Section.NG
            self.personal_schedule[date][Time.night] = Section.NG
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
    # これ何に使うんだっけ？
    def available_time(self, date, time:Time) -> bool:
        return True if self.personal_schedule[date][time] == Section.OFF else False
# スタッフ名簿
staffs = [
    Staff("浅田",   rank=16,     ng_request =[]),
    Staff("山本",   rank=16,     ng_request =[]),
    Staff("和田",   rank=18,    certified_section = [Section.s30594, Section.s30595], ng_request =[]),
    Staff("堀江",   rank=17,    certified_section = [Section.s30594, Section.s30595], ng_request =[]),
    Staff("佐藤拓", rank=12,    certified_section = [Section.s30594, Section.s30595], ng_request =[], is_phd = True),
    Staff("田上",   rank=12,    certified_section = [Section.s30594, Section.s30595], ng_request =[], is_phd = True),
    Staff("高井",   rank=10,    certified_section = [Section.s30594, Section.s30595, Section.s30596], ng_request =[], is_phd = True),
    Staff("水野",   rank=10,    certified_section = [Section.s30594, Section.s30595, Section.s30596], ng_request =[], is_phd = True),
    Staff("佐藤悠", rank= 8,    certified_section = [Section.s30594, Section.s30595, Section.s30596], ng_request =[]),
    Staff("中野",   rank= 6,    certified_section = [Section.s30594, Section.s30595, Section.s30596], ng_request =[]),
    Staff("木村",   rank= 6,    certified_section = [Section.s30594, Section.s30595, Section.s30596], ng_request =[]),
    Staff("有田",   rank= 6,    certified_section = [Section.s30594, Section.s30595], ng_request =[]),
    Staff("佐藤一", rank= 5,    certified_section = [Section.s30594, Section.s30595, Section.s30596], ng_request =[]),
    Staff("堂園",   rank= 5,    certified_section = [Section.s30594, Section.s30595, Section.s30596], ng_request =[]),
    Staff("池上",   rank= 4,    certified_section = [Section.s30594], ng_request =[]),
    Staff("谷本",   rank= 4,    ng_request =[]),
    Staff("川上",   rank= 3,    ng_request =[]),
    Staff("河田",   rank= 3,    ng_request =[]),
    Staff("野田",   rank= 3,    ng_request =[]),
    Staff("松山",   rank= 3,    ng_request =[]),
    Staff("諏江",   rank= 3,    ng_request =[]),
    Staff("瀧",     rank= 7,    ng_request =[]),
    # Staff("Kobayasi", rank= 3,    ng_request =[]),
    # Staff("Ikeda",    rank= 5,    ng_request =[]),
]
dummy_staff = Staff("Dummy", rank=10, certified_section = [Section.s30594, Section.s30595, Section.s30596], ng_request =[]),

def get_staff_by_name(name):
    staff = next((staff for staff in staffs if staff.name == name), None)
    if staff is None:
        raise ValueError(f"Staff with name {name} not found")
    return staff
class Monthly_schedules:
    def __init__(self) -> None:
        self.schedules = {}
        for date in target_cal:
            daily_assigns = {
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
            }}
            self.schedules[date] = daily_assigns
    def assign(self, date, time, section, name):
        staff = get_staff_by_name(name)
        time_category = Time.night if time == Time.night else Time.day
        check_isoff = (staff.personal_schedule[date][time_category] == Section.OFF)
        if not check_isoff:
            print(f"cannot assign {name} on {date},{time},{section}")
            return None
        if section in (Section.sEfree, Section.sIfree, Section.extras):
            self.schedules[date][time][section].append(name)
        else:
            self.schedules[date][time][section] = name

        if time == Time.extra:
            if section == Section.taitou:
                staff.extra_work_count += 2
                staff.personal_schedule[date][Time.day] = section
                staff.personal_schedule[date][Time.night] = section                
            else:
                staff.extra_work_count += 1
                staff.personal_schedule[date][Time.day] = section            
        elif time == Time.day:
            staff.work_count += 1
            staff.personal_schedule[date][time] = section
        elif time == Time.night:
            staff.work_count += 1.5
            staff.personal_schedule[date][time] = section
    def is_valid_assign(self, date) -> bool:
        staff_filled = all([self.schedules[date][Time.day][section] is not None for section in (Section.s30595, Section.s30599, Section.s30594, Section.s30596)] \
            + [self.schedules[date][Time.night][section] is not None for section in (Section.s30595, Section.s30599, Section.s30596)])
        
        day_staffs = [self.schedules[date][Time.day][section] for section in (Section.s30591, Section.s30595, Section.s30599, Section.s30594, Section.s30596, Section.s30597) if not None]\
                    + self.schedules[date][Time.day][Section.sIfree] + self.schedules[date][Time.day][Section.sEfree]
        night_staffs = [self.schedules[date][Time.night][section] for section in (Section.s30595, Section.s30599, Section.s30596) if not None]
        extra_staffs = [self.schedules[date][Time.extra][section] for section in (Section.sonoda, Section.teikyo, Section.mitsui, Section.taitou, Section.oomori, Section.chibat) if not None]\
                    + self.schedules[date][Time.extra][Section.extras]
        day_staff_not_conflicted = True if len(day_staffs + extra_staffs) == len(set(day_staffs + extra_staffs)) else False
        night_staff_not_conflicted = True if len(night_staffs + extra_staffs) == len(set(night_staffs + extra_staffs)) else False
        return all([staff_filled, day_staff_not_conflicted, night_staff_not_conflicted]) # 必須セクションが埋まっていること、日勤＋外勤に重複がないこと、夜勤＋外勤に重複がないこと
    def assignable_stafflist(self, date, time): # StaffではなくStaff.nameを返してるので注意
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
            {"main_section": Section.s30596, "sub_section": Section.s30597, "section_namelist": ["中野", "有田", "堂園", "池上"], "night_section": Section.s30596},
            {"main_section": Section.s30594, "sub_section": Section.sEfree, "section_namelist": ["佐藤悠", "木村", "佐藤一"], "night_section": Section.s30595}
        ]
        for item in icu_item:
            main_section = item["main_section"]
            sub_section = item["sub_section"]
            section_namelist = item["section_namelist"]
            night_section = item["night_section"]

            temp_staff_workcount_personal_schedules =  {staff.name: [deepcopy(staff.work_count), deepcopy(staff.personal_schedule)] for staff in staffs}
            new_monthly_schedules = deepcopy(self)
            complete_flag = False
            check_date = cal_begin
            for _ in range(100):
                print(f"\rnow solving {main_section}...{_+1}") # デバッグ用
                check_date = cal_begin
                restart_flag = False
                previous_staff_name = None
                while check_date <= cal_end:
                    print(f"checking {check_date}", end="")
                    if (cal_end - check_date).days <= 4:
                        block_assignable_stafflist = [[name, available_days, work_count] for name, available_days, work_count in self.block_assignable_stafflist(check_date, min_blockdate = (cal_end - check_date).days + 1) if name in section_namelist and name != previous_staff_name]
                    else: 
                        block_assignable_stafflist = [[name, available_days, work_count] for name, available_days, work_count in self.block_assignable_stafflist(check_date, min_blockdate = 5) if name in section_namelist and name != previous_staff_name]
                        if not block_assignable_stafflist:
                            block_assignable_stafflist = [[name, available_days, work_count] for name, available_days, work_count in self.block_assignable_stafflist(check_date, min_blockdate = 4) if name in section_namelist and name != previous_staff_name]
                            if not block_assignable_stafflist:
                                if previous_staff_name == "Dummy":
                                    restart_flag = True
                                    break
                                staff = dummy_staff
                                new_monthly_schedules.schedules[check_date][Time.day][main_section] = "Dummy"
                                previous_staff_name = "Dummy"
                                check_date += datetime.timedelta(days = 1)
                                continue
                    sorted_stafflist = sorted(block_assignable_stafflist, key=itemgetter(2))[:3]
                    for name, ad, wc in sorted_stafflist: # デバッグ用
                        print(f"{name}", end="")
                    name, available_days, wc = random.choice(sorted_stafflist)
                    staff = get_staff_by_name(name)
                    assign_block = min(5, available_days)
                    if check_date + datetime.timedelta(days = assign_block) > cal_end:
                        assign_block = (cal_end - check_date).days + 1
                        complete_flag = True
                    for i in range(assign_block):
                        if i == 0:
                            if check_date == cal_begin:
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
                    if complete_flag:
                        break
                if restart_flag:
                    # staff毎にwork_countとpersonal_schedulesをリセット
                    for staff in staffs:
                        staff.work_count, staff.personal_schedule = temp_staff_workcount_personal_schedules[staff.name]
                    new_monthly_schedules = deepcopy(self)
                    if _ == 99:
                        print("...cannot solved")
                else:
                    print(f"\r{main_section}...solved", end="")
                    break
            if complete_flag:
                self.schedules = new_monthly_schedules.schedules
        return complete_flag
    
    def assign_nightshifts(self):
        temp_staff_workcount_personal_schedules =  {staff.name: [deepcopy(staff.work_count), deepcopy(staff.personal_schedule)] for staff in staffs}
        for _ in range(100):
            print(f"\rnow solving night_shift...{_+1}", end="")
            new_monthly_schedules = deepcopy(self)
            incomplete_flag = False
            section_staff_namelists = {
                Section.s30595 : [staff.name for staff in staffs if Section.s30595 in staff.certified_section and not staff.is_phd],
                Section.s30596 : [staff.name for staff in staffs if Section.s30596 in staff.certified_section and not staff.is_phd],
                Section.s30599 : [staff.name for staff in staffs if staff.rank < 5]
            }
            section_help_namelists = {
                Section.s30595 : [staff.name for staff in staffs if Section.s30595 in staff.certified_section and staff.is_phd],
                Section.s30596 : [staff.name for staff in staffs if Section.s30596 in staff.certified_section and staff.is_phd],
                Section.s30599 : [staff.name for staff in staffs if Section.s30595 in staff.certified_section and not staff.is_phd]
            }
            for section in (Section.s30596, Section.s30595, Section.s30599):
                section_staff_namelist = section_staff_namelists[section]
                section_help_namelist = section_help_namelists[section]
                for date in target_cal:
                    # 既に割り振られてる場合はスキップ
                    if new_monthly_schedules.schedules[date][Time.night][section] is not None:
                        continue
                    daily_staffnames = [[name, work_count] for name, work_count in new_monthly_schedules.assignable_stafflist(date, Time.night) if name in section_staff_namelist]
                    if len(daily_staffnames) > 0:
                        daily_staffnames_less_work_count = sorted(daily_staffnames, key=itemgetter(1))[:3]
                        name, work_count = random.choice(daily_staffnames_less_work_count)
                        new_monthly_schedules.assign(date, Time.night, section, name)
                    else:
                        daily_help_staffnames = [[name, work_count] for name, work_count in new_monthly_schedules.assignable_stafflist(date, Time.night) if name in section_help_namelist]
                        print(f"\ndaily_help_staffnames: {daily_help_staffnames}")
                        if len(daily_help_staffnames) > 0:
                            daily_help_staffnames_less_work_count = sorted(daily_help_staffnames, key=itemgetter(1))[:3]
                            print(f"daily_help_staffnames_less_work_count: {daily_help_staffnames_less_work_count}")
                            name, work_count = random.choice(daily_help_staffnames_less_work_count)
                            new_monthly_schedules.assign(date, Time.night, section, name)
                        else:
                            print(f"none available on {date} for {section}")
                            incomplete_flag = True
                            break
                if incomplete_flag:
                    break
            if incomplete_flag:
                for staff in staffs:
                    staff.work_count, staff.personal_schedule = temp_staff_workcount_personal_schedules[staff.name]
                if _ == 99:
                    print("...cannot solved")
            else:
                self.schedules = new_monthly_schedules.schedules
                print(f"...solved")
                break
        return not incomplete_flag


def main():
    monthly_schedules = Monthly_schedules()
    monthly_schedules.assign_30591()
    flag = monthly_schedules.assign_icu_and_eicu()    
    flag = monthly_schedules.assign_nightshifts()
    print("")

    indexes = ["Date", "D_30591", "D_30595", "D_30599", "D_30594", "D_Efree", "D_30596", "D_30597", "D_Ifree", " ", "N_30595", "N_30599", "N_30596"]
    print("\t".join(indexes))
    print("")
    for date, schedule in monthly_schedules.schedules.items():
        output = [f"{date.strftime('%m-%d')}"]
        output.append(schedule[Time.day][Section.s30591] if schedule[Time.day][Section.s30591] else 'None')
        output.append(schedule[Time.day][Section.s30595] if schedule[Time.day][Section.s30595] else 'None')
        output.append(schedule[Time.day][Section.s30599] if schedule[Time.day][Section.s30599] else 'None')
        output.append(schedule[Time.day][Section.s30594] if schedule[Time.day][Section.s30594] else 'None')
        output.append(" ".join(schedule[Time.day][Section.sEfree]) if schedule[Time.day][Section.sEfree] else 'None')
        output.append(schedule[Time.day][Section.s30596] if schedule[Time.day][Section.s30596] else 'None')
        output.append(schedule[Time.day][Section.s30597] if schedule[Time.day][Section.s30597] else 'None')
        output.append(" ".join(schedule[Time.day][Section.sIfree]) if schedule[Time.day][Section.sIfree] else 'None')
        output.append(" ")
        output.append(schedule[Time.night][Section.s30595] if schedule[Time.night][Section.s30595] else 'None')
        output.append(schedule[Time.night][Section.s30599] if schedule[Time.night][Section.s30599] else 'None')
        output.append(schedule[Time.night][Section.s30596] if schedule[Time.night][Section.s30596] else 'None')
        print("\t".join(output))
    print("")
    '''
    indexes = ["Date", "苑田", "帝京", "三井", "大森", "台東", "千葉徳", "個人外勤"]
    print("\t".join(indexes))
    for date, schedule in monthly_schedules.schedules.items():
        output = [f"{date.strftime('%m-%d')}"]
        output.append(schedule[Time.extra][Section.sonoda] if schedule[Time.extra][Section.sonoda] else '\t')
        output.append(schedule[Time.extra][Section.teikyo] if schedule[Time.extra][Section.teikyo] else '\t')
        output.append(schedule[Time.extra][Section.mitsui] if schedule[Time.extra][Section.mitsui] else '\t')
        output.append(schedule[Time.extra][Section.oomori] if schedule[Time.extra][Section.oomori] else '\t')
        output.append(schedule[Time.extra][Section.taitou] if schedule[Time.extra][Section.taitou] else '\t')
        output.append(schedule[Time.extra][Section.chibat] if schedule[Time.extra][Section.chibat] else '\t')
        output.append(" ".join(schedule[Time.extra][Section.extras]) if schedule[Time.extra][Section.extras] else 'None')
        print("\t".join(output))
    '''
    for staff in staffs:
        print(f"{staff.name} works* {staff.work_count}", end="")
        actual_workcount = 0
        for date in target_cal:
            for section in (Section.s30591, Section.s30595, Section.s30599, Section.s30594, Section.s30596, Section.s30597):
                if monthly_schedules.schedules[date][Time.day][section] == staff.name:
                    actual_workcount += 1
            for section in (Section.sIfree, Section.sEfree):
                for listed_staff in monthly_schedules.schedules[date][Time.day][section]:
                    if listed_staff == staff.name:
                        actual_workcount += 1
            for section in (Section.s30596, Section.s30595, Section.s30599):
                if monthly_schedules.schedules[date][Time.night][section] == staff.name:
                    actual_workcount += 1.5
        print(f"({actual_workcount}), extra={staff.extra_work_count}")
main()