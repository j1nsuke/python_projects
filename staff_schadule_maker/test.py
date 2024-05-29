import random
import datetime
from enum import Enum

class Section(Enum):
    s30591 = "30591"
    s30595 = "30595"
    s30599 = "30599"
    s30596 = "30596"
    s30597 = "30597"
    sIfree = "Ifree"
    s30594 = '30594'
    sEfree = "Efree"
    
# カレンダーの用意
calendar = []
first_date = datetime.date(2024,6,1)
last_date = datetime.date(2024,6,30)
current_date = first_date
while current_date <= last_date:
    calendar.append(current_date)
    current_date += datetime.timedelta(days = 1)

class Staff():
    def __init__(self, name, rank, is_phd = False, assignable_section = None, icu_team = False, ng_request = None):
        self.name = name
        self.rank = rank
        self.is_phd = is_phd
        if assignable_section is None:
            assignable_section = []
        self.assignable_section = assignable_section
        self.icu_team = icu_team
        if ng_request is None:
            ng_request = []
        self.ng_request = ng_request
    
    def working_days(self):
        working_days = 0
        for date in calendar:
            daily_sections = Daily_sections(date)
            if self in daily_sections.day_staff.values():
                working_days += 1
            if self in daily_sections.night_staff.values():
                working_days += 1.5
        return working_days

# スタッフ名簿
staffs = [
    Staff("Asada", rank=16,   assignable_section = [Section.s30591, Section.s30595, Section.s30596], icu_team = True, ng_request =[]),
    Staff("Yamamoto", rank=16,   assignable_section = [Section.s30591, Section.s30595, Section.s30596], icu_team = True, ng_request =[]),
    Staff("Wada", rank=18,   assignable_section = [Section.s30595, Section.s30599, Section.s30594, Section.sEfree], ng_request =[]),
    Staff("Horie", rank=17,   assignable_section = [Section.s30595, Section.s30599, Section.s30594, Section.sEfree], ng_request =[]),
    Staff("SatoTaku", rank=12,   is_phd = True, assignable_section = [Section.s30595, Section.s30599, Section.s30594, Section.sEfree], ng_request =[]),
    Staff("Tagami", rank=12,   is_phd = True, assignable_section = [Section.s30595, Section.s30599, Section.s30594, Section.sEfree], ng_request =[]),
    Staff("Takai", rank=10,   is_phd = True, assignable_section = [Section.s30595, Section.s30599, Section.s30596, Section.s30597, Section.sIfree, Section.sEfree], icu_team = True, ng_request =[]),
    Staff("Mizuno", rank=10,   is_phd = True, assignable_section = [Section.s30595, Section.s30599, Section.s30594, Section.s30596, Section.s30597, Section.sIfree, Section.sEfree], ng_request =[]),
    Staff("SatoYuko", rank= 8,    assignable_section = [Section.s30595, Section.s30599, Section.s30596, Section.s30597, Section.sIfree], icu_team = True, ng_request =[]),
    Staff("Nakano", rank= 6,    assignable_section = [Section.s30595, Section.s30599, Section.s30596, Section.s30597, Section.sIfree], icu_team = True, ng_request =[]),
    Staff("Kimura", rank= 6,    assignable_section = [Section.s30595, Section.s30599, Section.s30596, Section.s30597, Section.sIfree], icu_team = True, ng_request =[]),
    Staff("Arita", rank= 6,    assignable_section = [Section.s30595, Section.s30599, Section.s30594, Section.sEfree], ng_request =[]),
    Staff("SatoKazu", rank= 5,    assignable_section = [Section.s30595, Section.s30599, Section.s30596, Section.s30597, Section.sIfree], icu_team = True, ng_request =[]),
    Staff("Dozono", rank= 5,    assignable_section = [Section.s30595, Section.s30599, Section.s30594, Section.sEfree, Section.s30596, Section.s30597, Section.sIfree], icu_team = True, ng_request =[]),
    Staff("Ikegami", rank= 4,    assignable_section = [Section.s30599, Section.sEfree], ng_request =[]),
    Staff("Tanimoto", rank= 4,    assignable_section = [Section.s30599, Section.sEfree, Section.s30597, Section.sIfree], icu_team = True, ng_request =[]),
    Staff("Kawakami", rank= 3,    assignable_section = [Section.s30599, Section.sEfree], ng_request =[]),
    Staff("Kawada", rank= 3,    assignable_section = [Section.s30599, Section.sEfree], ng_request =[]),
    Staff("Noda", rank= 3,    assignable_section = [Section.s30599, Section.sEfree], ng_request =[]),
    Staff("Matuyama", rank= 3,    assignable_section = [Section.s30599, Section.sEfree], ng_request =[]),
    Staff("Sue", rank= 3,    assignable_section = [Section.s30599, Section.sEfree], ng_request =[]),
    Staff("Taki", rank= 7,    assignable_section = [Section.s30599, Section.sEfree], ng_request =[]),
    Staff("Kobayasi", rank= 3,    assignable_section = [Section.s30599, Section.sEfree], ng_request =[]),
    Staff("Ikeda", rank= 5,    assignable_section = [Section.s30599, Section.sEfree], ng_request =[]),
]

def get_staff(name):
    return next((staff for staff in staffs if staff.name == name), None)

class Daily_sections:
    def __init__(self, date:datetime.date) -> None:
        self.date = date
        self.day_staff = {
                            Section.s30591: None,
                            Section.s30595: None,
                            Section.s30599: None,
                            Section.s30596: None,
                            Section.s30597: None,
                            Section.sIfree: [],
                            Section.s30594: None,
                            Section.sEfree: []
        }
        self.night_staff ={
                            Section.s30595: None,
                            Section.s30599: None,
                            Section.s30596: None
        }
    
    def find_assignable_staffs(self, previous_night_staffs):
        date = self.date
        daily_assignable_staffs = []
        day_assignable = []
        night_assignable = []
        next_date = date + datetime.timedelta(days = 1)
        for staff in staffs:
            if date not in staff.ng_request:
                day_assignable.append(staff)
                if next_date not in staff.ng_request:
                    night_assignable.append(staff)
            #定期外勤を除外
            #月曜日
            if date.weekday() == 0:
                if staff.name in ("Tagami", "Wada"):
                    night_assignable.remove(staff)
            #火曜日          
            if date.weekday() == 1:
                if staff.name in ("Tagami", "Wada"):
                    day_assignable.remove(staff)
                    night_assignable.remove(staff)
                if staff.name in ("Asada"):
                    night_assignable.remove(staff)
            #水曜日          
            if date.weekday() == 3:
                if staff.name in ("Asada"):
                    day_assignable.remove(staff)
                    night_assignable.remove(staff)
                if staff.name in ("Mizuno"):
                    night_assignable.remove(staff)
            #木曜日          
            if date.weekday() == 4:
                if staff.name in ("Mizuno"):
                    day_assignable.remove(staff)
                    night_assignable.remove(staff)
                if staff.name in ("Tagami", "SatoTaku"):
                    night_assignable.remove(staff)
            #金曜日          
            if date.weekday() == 5:
                if staff.name in ("Tagami", "SatoTaku"):
                    day_assignable.remove(staff)
                    night_assignable.remove(staff)

        for staff in previous_night_staffs:
            if staff in day_assignable:
                day_assignable.remove(staff)
            if staff in night_assignable:
                night_assignable.remove(staff)

        daily_assignable_staffs = [day_assignable, night_assignable]
        return daily_assignable_staffs

    def assign_algorithm(self, section: Section, daily_assignable_staffs):
        daily_staff = daily_assignable_staffs
        if self.day_staff[section] is None:
            d_staff = random.choice(daily_staff[0])
            if section in d_staff.assignable_section:
                self.day_staff[section] = d_staff
                daily_staff[0].remove(d_staff)
        if section in (Section.s30595, Section.s30599, Section.s30596):
            if self.night_staff[section] is None:
                if self.day_staff[section] in daily_staff[1]:
                    n_staff = self.day_staff[section]
                else:
                    for _ in range(100):
                        n_staff = random.choice(daily_staff[1])
                        if section in n_staff.assignable_section:
                            break
                self.night_staff[section] = n_staff
                daily_staff[1].remove(n_staff)
        return self, daily_assignable_staffs

    def assign_yamamoto(self, daily_assignable_staffs):
        date = self.date
        staff = get_staff("Yamamoto")
        if staff not in daily_assignable_staffs:
            print(f"cannot assign Yamamoto on {date}")
        else:
            if date.weekday() in (1, 2, 3): #火水木の日勤30591→山本
                self.day_staff[Section.s30591] = staff
            if date.weekday() == 6: #日の夜勤30596→山本
                self.night_staff[Section.s30596] = staff
    
    def assign_asada(self, daily_assignable_staffs):
        date = self.date
        staff = get_staff("Asada")
        if staff not in daily_assignable_staffs:
            print(f"cannot assign Asada on {date}")
        else:
            if date.weekday() in (0, 4): #月金の日勤30591→浅田
                self.day_staff[Section.s30591] = staff
    
    

        



    def assign_main_staffs(self, daily_assignable_staffs):
        for i in range(100):
            if self.section_filled():
                break
            #30591　日勤        平日のみ
            if self.is_weekday():
                self, daily_assignable_staffs = self.assign_algorithm(Section.s30591, daily_assignable_staffs)
            #30596　日勤、夜勤
            self, daily_assignable_staffs = self.assign_algorithm(Section.s30596, daily_assignable_staffs)
            #30597　日勤
            self, daily_assignable_staffs = self.assign_algorithm(Section.s30597, daily_assignable_staffs)
            #30595　日勤、夜勤
            self, daily_assignable_staffs = self.assign_algorithm(Section.s30595, daily_assignable_staffs)
            #30594　日勤
            self, daily_assignable_staffs = self.assign_algorithm(Section.s30594, daily_assignable_staffs)
            #30599　日勤、夜勤
            self, daily_assignable_staffs = self.assign_algorithm(Section.s30599, daily_assignable_staffs)
    '''
    # EICU, ICU free
    def assign_sub_staff(self, daily_assignable_staffs):
        daily_staff = daily_assignable_staffs
        staff = random.choice(daily_staff[0])
        if staff.icu_team == True:
            self.day_staff[Section.d_Ifree].append(staff)
        else:
            self.day_staff[Section.d_Efree].append(staff)
    '''
    def section_filled(self)->bool:
        return all([
            self.day_staff[Section.s30594] is not None,
            self.day_staff[Section.s30596] is not None,
            self.day_staff[Section.s30597] is not None,
            self.day_staff[Section.s30595] is not None,
            self.day_staff[Section.s30599] is not None,
            self.night_staff[Section.s30596] is not None,
            self.night_staff[Section.s30595] is not None,
            self.night_staff[Section.s30599] is not None,
            not self.is_weekday() or self.day_staff[Section.s30591] is not None
            ])
    
    def is_weekday(self)->bool:
        return self.date.weekday() < 5

def main():
    cal_daily_section = []
    for date in calendar:
        if date == first_date:
            previous_night_staffs = []
        daily_sections = Daily_sections(date)
        daily_assignable_staffs = daily_sections.find_assignable_staffs(previous_night_staffs)
        daily_sections.assign_main_staffs(daily_assignable_staffs)
        #daily_sections.assign_sub_staff(daily_assignable_staffs)
        cal_daily_section.append({date: daily_sections})
        previous_night_staffs = []
        for section, staff in daily_sections.night_staff.items():
            previous_night_staffs.append(staff)

    indexes = ["Date", "D_30591", "D_30595", "D_30599", "D_30594", "D_Efree", "D_30596", "D_30597", "D_Ifree", "N_30595", "N_30599", "N_30596"]
    for index in indexes:
        print(f"{index}", end="\t")
    print("")
    for entry in cal_daily_section:
        for date, daily_sections in entry.items():
            output = [f"{date.strftime('%m-%d')}"]
            output.append(f"{daily_sections.day_staff[Section.s30591].name if daily_sections.day_staff[Section.s30591] else 'None'}")
            output.append(f"{daily_sections.day_staff[Section.s30595].name if daily_sections.day_staff[Section.s30595] else 'None'}")
            output.append(f"{daily_sections.day_staff[Section.s30599].name if daily_sections.day_staff[Section.s30599] else 'None'}")
            output.append(f"{daily_sections.day_staff[Section.s30594].name if daily_sections.day_staff[Section.s30594] else 'None'}")
            output.append(f"{' '.join([staff.name for staff in daily_sections.day_staff[Section.sEfree]]) if daily_sections.day_staff[Section.sEfree] else 'None'}")
            output.append(f"{daily_sections.day_staff[Section.s30596].name if daily_sections.day_staff[Section.s30596] else 'None'}")
            output.append(f"{daily_sections.day_staff[Section.s30597].name if daily_sections.day_staff[Section.s30597] else 'None'}")
            output.append(f"{' '.join([staff.name for staff in daily_sections.day_staff[Section.sIfree]]) if daily_sections.day_staff[Section.sIfree] else 'None'}")
            output.append(f"{daily_sections.night_staff[Section.s30595].name if daily_sections.night_staff[Section.s30595] else 'None'}")
            output.append(f"{daily_sections.night_staff[Section.s30599].name if daily_sections.night_staff[Section.s30599] else 'None'}")
            output.append(f"{daily_sections.night_staff[Section.s30596].name if daily_sections.night_staff[Section.s30596] else 'None'}")
            print("\t".join(output))

main()