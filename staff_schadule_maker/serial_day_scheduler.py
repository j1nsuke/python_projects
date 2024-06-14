import random
import datetime
from operator import attrgetter

cal_start = datetime.date(2024, 7, 1)
cal_end = datetime.date(2024, 9, 30)
current_date = cal_start
cal = []
while current_date <= cal_end:
    cal.append(current_date)
    current_date += datetime.timedelta(days=1)

class Staff:
    def __init__(self, name: str) -> None:
        self.name = name
        self.ng_date = sorted(random.sample(cal, 6))
        self.work_count = 0

dr_list = []
for i in range(5):
    name = f"dr.{i}"
    dr = Staff(name)
    dr_list.append(dr)
for dr in dr_list:
    print(f"{dr.name}", end="\t")
    for date in dr.ng_date:
        print(f"{date.strftime('%m-%d')}", end=", ")
    print("")

# 目的のcalの期間を埋めるための勤務表を考える
# 連勤するほうが良いので4～5日毎の連勤を考える
# 前の勤務者の連勤最終日には、引継ぎのために後の勤務者を副勤務としてあてよう
# 連勤最終日の次の日も疲れているから、そこにng_dateがあたらないようにする

cal_list = {}
for dr in dr_list:
    workable_dates = []
    for i in range(len(dr.ng_date)+1):
        start_date = cal_start if i == 0 else dr.ng_date[i-1] + datetime.timedelta(days=1)
        end_date = cal_end if i == len(dr.ng_date) else dr.ng_date[i] - datetime.timedelta(days=1)
        # 差が4日＝その区間は5日、4連勤(597->596*3)+明けを設定できる
        if end_date - start_date > datetime.timedelta(days=4):
            workable_date = start_date
            while workable_date <= end_date:
                workable_dates.append(workable_date)
                workable_date += datetime.timedelta(days = 1)
    cal_list[dr] = workable_dates

# 勤務できるヒトが0人、1人の日があると成り立たないだろうから先にチェックしておこう
def cal_checker(cal_list):
    cal_count = {date: 0 for date in cal}
    for workable_dates in cal_list.values():
        for date in workable_dates:
            cal_count[date] += 1

    for date, count in cal_count.items():
        if count == 0:
            print(f"0 person on {date}")
        if count == 1:
            print(f"1 person on {date}")
cal_checker(cal_list)

def staff_picker(cal_list, check_date, previous_dr):
    # 先に連勤が最終日をはみ出したときの例外処理をしておこう
    cal_limit = False
    cal_limit_days = None
    if cal_end - check_date < datetime.timedelta(days = 5):
        cal_limit = True
        cal_limit_days = cal_end - check_date
    if not cal_limit:
        # 連勤最終日の次の日も疲れているから、そこにng_dateがあたらないようにすると5連勤なら6日間、4連勤なら5日間チェックする必要がある
        # 同じヒトが連続してあてられてはいけないから除外する
        workable_5days_dr_list = [dr for dr, date in cal_list.items() if dr != previous_dr and check_date in date and check_date + datetime.timedelta(days=5) in date]
        workable_4days_dr_list = [dr for dr, date in cal_list.items() if dr != previous_dr and check_date in date and check_date + datetime.timedelta(days=4) in date]
        workable_5days_dr_list.sort(key=attrgetter("work_count"))
        workable_4days_dr_list.sort(key=attrgetter("work_count"))
        workable_5days_dr_list = workable_5days_dr_list[:2]
        workable_4days_dr_list = workable_4days_dr_list[:2]
        # 連勤初日は副勤務者になるから、5連勤なら主勤務者として働くのは4日、4連勤なら3日になる
        if len(workable_5days_dr_list) > 0:
            selected_dr = random.choice(workable_5days_dr_list)
            selected_term = 4
        elif len(workable_4days_dr_list) > 0:
            selected_dr = random.choice(workable_4days_dr_list)
            selected_term = 3
        else:
            selected_dr = None
            selected_term = None
    else:
        workable_dr_list = [dr for dr, date in cal_list.items() if check_date in date and cal_end in date]
        if len (workable_dr_list) > 0:
            selected_dr = random.choice(workable_dr_list)
            selected_term = cal_limit_days.days
        else:
            selected_dr = None
            selected_term = None
    return selected_dr, selected_term, cal_limit

def staff_picker(self, temp_matrix, check_date, previous_dr, staff_names):
    # 先に連勤が最終日をはみ出したときの例外処理をしておこう
    cal_limit = False
    cal_limit_days = None
    if last_date - check_date < datetime.timedelta(days = 5):
        cal_limit = True
        cal_limit_days = last_date - check_date
    if not cal_limit:
        # 連勤最終日の次の日も疲れているから、そこにng_dateがあたらないようにすると5連勤なら6日間、4連勤なら5日間チェックする必要がある
        # 同じヒトが連続してあてられてはいけないから除外する
        workable_5days_dr_list = [staff for staff in staffs if staff.name in staff_names and staff != previous_dr and check_date in temp_matrix.daily_assignable_staffs(check_date)[0] and check_date + datetime.timedelta(days=5) in temp_matrix.daily_assignable_staffs(check_date + datetime.timedelta(days=5))[0]]
        workable_4days_dr_list = [staff for staff in staffs if staff.name in staff_names and staff != previous_dr and check_date in temp_matrix.daily_assignable_staffs(check_date)[0] and check_date + datetime.timedelta(days=4) in temp_matrix.daily_assignable_staffs(check_date + datetime.timedelta(days=4))[0]]
        workable_5days_dr_list.sort(key=attrgetter("work_count"))
        workable_4days_dr_list.sort(key=attrgetter("work_count"))
        workable_5days_dr_list = workable_5days_dr_list[:2]
        workable_4days_dr_list = workable_4days_dr_list[:2]
        # 連勤初日は副勤務者になるから、5連勤なら主勤務者として働くのは4日、4連勤なら3日になる
        if len(workable_5days_dr_list) > 0:
            selected_dr = random.choice(workable_5days_dr_list)
            selected_term = 4
        elif len(workable_4days_dr_list) > 0:
            selected_dr = random.choice(workable_4days_dr_list)
            selected_term = 3
        else:
            selected_dr = None
            selected_term = None
    else:
        workable_dr_list = [staff for staff in staffs if staff.name in staff_names and check_date in temp_matrix.daily_assignable_staffs(check_date)[0] and last_date in temp_matrix.daily_assignable_staffs(last_date)[0]]
        if len(workable_dr_list) > 0:
            selected_dr = random.choice(workable_dr_list)
            selected_term = cal_limit_days.days
        else:
            selected_dr = None
            selected_term = None
    return selected_dr, selected_term, cal_limit







for _ in range(100):
    schedules = []
    incomplete_flag = False
    check_date = cal_start
    previous_dr = dr_list[0]
    while check_date <= cal_end:
        dr, term, cal_limit = staff_picker(cal_list, check_date, previous_dr)
        if dr is None:
            incomplete_flag = True
            break
        else:
            dr_term = [dr, term]
            schedules.append(dr_term)
            dr.work_count += term + 1
            if cal_limit:
                break
            else:
                check_date += datetime.timedelta(days = term - 1)
                previous_dr = dr
    if incomplete_flag:
        print(f"failed in trial {_+1}")
        continue
    else:
        print("Done!")
        for name_term in schedules:
            print(f"{name_term[0].name}: {name_term[1]}")
        for dr in dr_list:
            print(f"{dr.name}: workcount {dr.work_count}")
        break
