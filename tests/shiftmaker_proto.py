import calendar
import datetime
import random
import statistics
from collections import defaultdict
from operator import itemgetter
from enum import Enum
from copy import deepcopy

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

#　変数部分
target_ym = Target_year_month(year = 2024, month = 6)
req_list = [
    Request("Dr1", Role.ER, 1, [2, 26, 13, 9], [10, 14, 22, 25, 26, 20]),
    Request("Dr2", Role.ER, 1, [4, 27, 25, 23], [9, 5, 18, 3, 30, 19]),
    Request("Dr3", Role.ER, 1, [17, 22, 16, 2], [26, 24, 17, 28, 22, 21]),
    Request("Dr4", Role.ER, 0, [21, 13, 19, 29], [4, 15, 27, 13, 21, 22]),
    Request("Dr5", Role.ER, 1, [2, 7], [12, 26, 19, 10, 2, 3]),
    Request("Dr6", Role.ER, 2, [15, 12, 1, 24], [10, 13, 24, 16, 8, 1]),
    Request("Dr7", Role.ER, 2, [13, 12, 18, 20], [19, 3, 9, 11, 10, 25]),
    Request("Dr8", Role.ER, 0, [4], [15, 23, 26, 8, 10, 18]),
    Request("Dr9", Role.ER, 2, [23, 5, 9, 14], [13, 24, 30, 10, 14, 18]),
    Request("Dr10", Role.ER, 1, [18, 22, 10, 5], [3, 26, 5, 2, 11, 27]),
    Request("Dr11", Role.ER, 2, [3, 21,  28], [6, 18, 12, 17, 11, 21]),
    Request("Dr12", Role.ER, 1, [6, 22, 16, 2], [10, 5, 7, 11, 20, 27]),
    Request("Dr13", Role.ER, 0, [29, 27, 23, 10], [21, 14, 8, 15, 5, 9]),
    Request("Dr14", Role.ER, 0, [25, 11], [14, 17, 26, 22, 24, 3]),
    Request("Dr15", Role.ER, 2, [19, 12, 1, 3], [16, 8, 26, 4, 19, 12]),
    Request("Dr16", Role.ICU, 2, [15, 23], [26, 19, 10, 21, 25, 9]),
    Request("Dr17", Role.ICU, 1, [7, 12, 6, 13], [5, 6, 8, 17, 12, 21]),
    Request("Dr18", Role.ICU, 2, [9, 19, 16, 13], [1, 2, 17, 19, 13, 16]),
    Request("Dr19", Role.ICU, 0, [10, 13, 11, 27], [20, 29, 21, 11, 17, 28]),
    Request("Dr20", Role.ICU, 0, [12, 5, 30, 1], [14, 6, 29, 26, 1, 21]),
]
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
monthly_requests = Convert_to_date(req_list, target_ym.year, target_ym.month)

#########################InternSchedule.py###########################
class InternSchedule:
    def __init__(self, intern: Request, target_ym: Target_year_month):
        self.intern = intern
        self.name = intern.name
        self.role = intern.role
        self.year = target_ym.year
        self.month = target_ym.month
        self.schedule = {(datetime.date(self.year, self.month, day)): Section.OFF for day in range(1, self.days_in_month() + 1)}
        self.datelist = [datetime.date(self.year, self.month, day) for day in range(1, self.days_in_month() + 1)]
        for ng_date in self.intern.ng_dates:
            self.schedule[ng_date] = Section.NG_A
        self.protoschedule = self.schedule

    def days_in_month(self) -> int:
        return calendar.monthrange(self.year, self.month)[1]

    def find_NER_assignable(self):
        NER_assignable = []
        for day in self.datelist:
            if day == datetime.date(self.year, self.month, self.days_in_month()):
                if self.schedule[day] == Section.OFF:
                    NER_assignable.append(day) 
            else:
                next_day = day + datetime.timedelta(days = 1)
                if self.schedule[day] == Section.OFF and self.schedule[next_day] == Section.OFF:
                    NER_assignable.append(day)
        return NER_assignable

    def assign_schedule(self):
        protoschedule = deepcopy(self.protoschedule)
        for trial in range (500):
            restart = False
            self.schedule = deepcopy(protoschedule)
            if self.intern.role == Role.ER: # ERの勤務を順にランダムに割り付け
                # EICUを割り当て
                for _ in range(6):
                    while True:
                        random_day = datetime.date(self.year, self.month, random.randint(1, self.days_in_month()))
                        if self.schedule[random_day] == Section.OFF:
                            self.schedule[random_day] = Section.EICU
                            break
                # ERを割り当て
                for _ in range(6 - self.intern.paidoff):
                    while True:
                        random_day = datetime.date(self.year, self.month, random.randint(1, self.days_in_month()))
                        if self.schedule[random_day] == Section.OFF:
                            self.schedule[random_day] = Section.ER
                            break

            if self.intern.role == Role.ICU: #　ICUの勤務をランダムに割り付け
                # ICUを割り当て
                for _ in range(17 - self.intern.paidoff):
                    while True:
                        random_day = datetime.date(self.year, self.month, random.randint(1, self.days_in_month()))
                        if self.schedule[random_day] == Section.OFF:
                            self.schedule[random_day] = Section.ICU
                            break

            if self.intern.role == Role.ER: #　NERをわりつけ
                for _ in range(6):
                    if len(self.find_NER_assignable()) == 0:
                        restart = True
                    else:
                        random_day = random.choice(self.find_NER_assignable())
                        self.schedule[random_day] = Section.NER

            if self.intern.role == Role.ICU: #　NERをわりつけ
                for _ in range(3):
                    if len(self.find_NER_assignable()) == 0:
                        restart = True
                    else:
                        random_day = random.choice(self.find_NER_assignable())
                        self.schedule[random_day] = Section.NER

            if self.is_valid() and restart == False: # 禁則（6連勤以上またはNER→OFFでない）パターンの勤務はやりなおし、かつ夜勤が割り振れていれば
                break
        return self.schedule
    
    def is_off(self, date: datetime.date) -> bool:
        return self.schedule[date] in [Section.OFF, Section.NG_A, Section.NG_B]
    
    def section_count(self, section: Section):
        count = 0
        for date in self.schedule:
            if self.schedule[date] == section:
                count += 1
        return count

    def is_valid(self)-> bool: # 禁則：6連勤以上または夜勤後に勤務/有休パターンを排除

        CONSEQUTIVE_WORK_LIMIT = 6
        count = 0

        for date in self.datelist:
            if not self.is_off(date):
                count += 1
            else:
                count = 0
            if count >= CONSEQUTIVE_WORK_LIMIT:
                return False
        
        for i, current_date in enumerate(self.datelist):
            next_date = self.datelist[i + 1] if i + 1 < len(self.datelist) else None
            if self.schedule[current_date] == Section.NER:
                if next_date and not self.schedule[next_date] == Section.OFF:
                    return False
        
        for date in self.datelist:
            if not date == datetime.date(self.year, self.month, self.days_in_month()):
                next_day = date + datetime.timedelta(days = 1)
                if self.schedule[date] == Section.NER and not self.schedule[next_day] == Section.OFF:
                    return False

        return True

    def print_workcount(self):
        ER_count = self.section_count(Section.ER)
        EICU_count = self.section_count(Section.EICU)
        ICU_count = self.section_count(Section.ICU)
        NER_count = self.section_count(Section.NER)
        NG_A_count = self.section_count(Section.NG_A)
        satisfaction = self.satisfaction()
        print(f"{self.name}...EICU: {EICU_count}, ER: {ER_count}, ICU: {ICU_count}, NER: {NER_count}, PaidOFF: {NG_A_count}, satisfaction: {satisfaction}")
    
    def satisfaction(self):
        score = 0
        consequtive_EICU_count = 0
        EICU_one_miss = False
        consequtive_off_count = 0
        for date in self.datelist:
            # 週末の勤務で -5
            if not self.is_off(date) and date.weekday() in (5,6):
                score -= 5
            # EICU連続勤務で加点 2連 +1 3連 +4 4連 +9 5連 +16　
            if self.schedule[date] == Section.EICU:
                consequtive_EICU_count += 1
                score += (consequtive_EICU_count - 1)**2
                EICU_one_miss = True
            else: # EICU 1回スキップは連勤カウントに含める
                if EICU_one_miss == True:
                    EICU_one_miss = False
                else:
                    consequtive_EICU_count = 0
            # 連続休暇で 2連 +1 3連 +8 4連 +27
            if self.is_off(date):
                consequtive_off_count += 1
                score += (consequtive_off_count - 1)**3
            else:
                consequtive_off_count = 0
            # NG_Bがoffなら +8
            if self.is_off(date) and date in self.intern.extra_ng_dates:
                score += 8
        return score
                    
############## evaluator ##############
# 日毎のsection充足度の評価関数
def calc_daily_section_counts(team_schedules, weekday_target_counts, weekend_target_counts):
    daily_section_counts = defaultdict(lambda: defaultdict(int))
    daily_section_diffs = defaultdict(lambda: defaultdict(int))
    
    for intern in team_schedules:
        for date, section in intern.schedule.items():
            if section in (Section.NER, Section.ICU, Section.EICU, Section.ER):
                daily_section_counts[date][section] += 1

    daily_scores = {}
    for date, section in intern.schedule.items():
        score = 0
        weekday = date.weekday()
        target_counts = weekday_target_counts if weekday < 5 else weekend_target_counts  # 平日と週末で目標人数を切り替える
        for section in (Section.NER, Section.ICU, Section.EICU, Section.ER):
            count = daily_section_counts[date][section]
            diff = (target_counts[section] - count)
            daily_section_diffs[date][section] = diff
            shortage = max(0, diff)
            score += shortage
        daily_scores[date] = score

    calc_scores = sum(daily_scores.values())
    return daily_section_counts, daily_section_diffs, calc_scores

# 研修医ごとのシフトへの満足度…はInternSchedule()に組み込んでしまったので、その統計処理
def intern_satisfaction_stats(team_schedules):
    intern_satisfactions = []
    for intern in team_schedules:
        score = intern.satisfaction()
        intern_satisfactions.append(score)
    
    total_score = sum(intern_satisfactions)
    stdev = statistics.stdev(intern_satisfactions)

    return total_score, stdev

##############　modifier　##############
#swap_A_B()の実装
def swap_A_B(team_schedules, bigger_date, smaller_date, sectionA: Section, sectionB: Section):
    for intern in team_schedules:
        if intern.schedule[bigger_date] == sectionA and intern.schedule[smaller_date] == sectionB:
            intern.schedule[bigger_date] = sectionB
            intern.schedule[smaller_date] = sectionA
            if intern.is_valid():
                break
            else:
                intern.schedule[bigger_date] = sectionA
                intern.schedule[smaller_date] = sectionB            
                for _ in range(50): # bigger, smallerのペアだけで改善出来ない、勤務者なしの部分をうめてるのかな？
                    rand_date = random.choice(team_schedules[0].datelist)
                    if intern.schedule[rand_date] == sectionA and intern.schedule[smaller_date] == sectionB:
                        intern.schedule[rand_date] = sectionB
                        intern.schedule[smaller_date] = sectionA
                        if intern.is_valid():
                            break
                        else:
                            intern.schedule[rand_date] = sectionA
                            intern.schedule[smaller_date] = sectionB
                    elif intern.schedule[bigger_date] == sectionA and intern.schedule[rand_date] == sectionB:
                        intern.schedule[bigger_date] = sectionB
                        intern.schedule[rand_date] = sectionA
                        if intern.is_valid():
                            break
                        else:
                            intern.schedule[bigger_date] = sectionA
                            intern.schedule[rand_date] = sectionB
                    else:
                        continue
                    break
    return team_schedules

# ranking_swap_schedule() shortageを順位付けして勤務を見つける手法
def ranking_swap_schedule(team_schedules, weekday_target_counts, weekend_target_counts, iterations=300):
    improvements = []
    team_schedules = deepcopy(team_schedules)
    for k in range(iterations):
        init_sec_counts, init_sec_diffs, init_scores = calc_daily_section_counts(team_schedules, weekday_target_counts, weekend_target_counts)
        
        section_date_diff_rank = defaultdict(list)
        for section in (Section.NER, Section.EICU, Section.ER, Section.NER):
            date_diffs = {date: diff[section] for date, diff in init_sec_diffs.items() if section in diff}
            sorted_date_diffs = sorted(date_diffs.items(), key=lambda item: item[1])
            section_date_diff_rank[section] = sorted_date_diffs

        for section in (Section.NER, Section.EICU, Section.ER, Section.NER):
            sorted_diffs = section_date_diff_rank[section]
            if sorted_diffs:
                bigger_date, bigger_diff = sorted_diffs[0] # sortedで大きい方=diffが小さい=余分に勤務者がいる
                smaller_date, smaller_diff = sorted_diffs[-1]
                new_team_schedules = swap_A_B(team_schedules, bigger_date, smaller_date, section, Section.OFF)

        new_sec_counts, new_sec_diffs,  new_scores = calc_daily_section_counts(new_team_schedules, weekday_target_counts, weekend_target_counts)
        improvement = init_scores - new_scores
        improvements.append(improvement)
        if improvement > 0:
            team_schedules = new_team_schedules
            final_sec_counts = new_sec_counts
            final_sec_diffs = new_sec_diffs
            final_scores = new_scores
            
    return team_schedules, final_sec_counts, final_scores, improvements

# ranking_swap_schedule()の実行, スコアの印刷, 改善度の印刷
many_schedules = []
for i in range(20):
    initial_team_schedules = []
    for request in monthly_requests:
        intern_schedule = InternSchedule(request, target_ym)
        intern_schedule.assign_schedule()
        initial_team_schedules.append(intern_schedule)
    for j in range(5):
        temp_team_schedules, temp_sec_counts, temp_score, improvement_history = ranking_swap_schedule(initial_team_schedules, weekday_target_counts, weekend_target_counts)
        print(f"\rnow producing schedule samples...{i*5 + j + 1}/100", end="")
        satisfaction_score, satisfaction_stdev = intern_satisfaction_stats(temp_team_schedules)
        trial = f"Trial{i*5 + j + 1}"
        temp = [trial, temp_score, satisfaction_stdev, satisfaction_score, temp_team_schedules, temp_sec_counts]
        many_schedules.append(temp)
print("")

many_schedules.sort(key=itemgetter(1,2))
for temp in many_schedules:
    print(f"{temp[0]}...SectionErr: {temp[1]}, Intern_stdev: {temp[2]:.2f}, Intern_sum:{temp[3]}")

print("================================================")

top3_schedules = []
for _ in range(3):
    final_team_schedules = many_schedules[_][4]
    final_sec_counts = many_schedules[_][5]
    final = [final_team_schedules, final_sec_counts]
    top3_schedules.append(final)

for finals in top3_schedules:
    final_team_schedules = finals[0]
    final_sec_counts = finals[1]
    for intern in final_team_schedules:
        print(f"{intern.name} {intern.role}, ", end='')
        for date, value in intern.schedule.items():
            print(f"{value.value}", end=',')
        print('')

    for date, section_counts in sorted(final_sec_counts.items()):
        print(f"Date: {date} ", end='')
        for section, count in sorted(section_counts.items(), key=lambda x: x[0].name):
            print(f"{section.name}: {count}", end=", ")
        print('')

    for intern in final_team_schedules:
        intern.print_workcount()
    print("================================================")
