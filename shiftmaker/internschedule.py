import calendar
import datetime
import random
from copy import deepcopy
from lib import *

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

    def assign_schedule(self, work_counts):
        protoschedule = deepcopy(self.protoschedule)
        for trial in range (500):
            restart = False
            self.schedule = deepcopy(protoschedule)
            if self.intern.role == Role.ER: # ERの勤務を順にランダムに割り付け
                # EICUを割り当て
                for _ in range(work_counts[self.intern.role][Section.EICU]):
                    while True:
                        random_day = datetime.date(self.year, self.month, random.randint(1, self.days_in_month()))
                        if self.schedule[random_day] == Section.OFF:
                            self.schedule[random_day] = Section.EICU
                            break
                # ERを割り当て
                for _ in range(work_counts[self.intern.role][Section.ER] - self.intern.paidoff):
                    while True:
                        random_day = datetime.date(self.year, self.month, random.randint(1, self.days_in_month()))
                        if self.schedule[random_day] == Section.OFF:
                            self.schedule[random_day] = Section.ER
                            break

            if self.intern.role == Role.ICU: #　ICUの勤務をランダムに割り付け
                # ICUを割り当て
                for _ in range(work_counts[self.intern.role][Section.ICU] - self.intern.paidoff):
                    while True:
                        random_day = datetime.date(self.year, self.month, random.randint(1, self.days_in_month()))
                        if self.schedule[random_day] == Section.OFF:
                            self.schedule[random_day] = Section.ICU
                            break

            if self.intern.role == Role.ER: #　NERをわりつけ
                for _ in range(work_counts[self.intern.role][Section.NER]):
                    if len(self.find_NER_assignable()) == 0:
                        restart = True
                    else:
                        random_day = random.choice(self.find_NER_assignable())
                        self.schedule[random_day] = Section.NER

            if self.intern.role == Role.ICU: #　NERをわりつけ
                for _ in range(work_counts[self.intern.role][Section.NER]):
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
    
    def set_NG_B(self):
        for date in self.intern.extra_ng_dates:
            if self.schedule[date] == Section.OFF:
                self.schedule[date] = Section.NG_B

    def print_workcount(self):
        ER_count = self.section_count(Section.ER)
        EICU_count = self.section_count(Section.EICU)
        ICU_count = self.section_count(Section.ICU)
        NER_count = self.section_count(Section.NER)
        # NG_A_count = self.section_count(Section.NG_A)
        satisfaction = self.satisfaction()
        print(f"{self.name}...EICU: {EICU_count}, ER: {ER_count}, ICU: {ICU_count}, NER: {NER_count}, PaidOFF: {self.intern.paidoff}, satisfaction: {satisfaction}")
    
    def satisfaction(self):
        score = 0
        consequtive_EICU_count = 0
        EICU_one_miss = False
        consequtive_off_count = 0
        for date in self.datelist:
            # 週末の勤務で -10
            if not self.is_off(date) and date.weekday() in (5,6):
                score -= 10
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
            # NG_Bがoffなら +15
            if self.is_off(date) and date in self.intern.extra_ng_dates:
                score += 15
        return score