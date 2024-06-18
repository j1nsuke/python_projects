import argparse
import datetime
from operator import itemgetter
from lib import *
from internschedule import InternSchedule
from evaluator import calc_daily_section_counts, intern_satisfaction_stats
from modifier import ranking_swap_schedule

#　変数部分
req_list = [
    Request("Sugimoto", Role.ER, 3, [5, 6, 13, 26, 29], [27, 28, 20, 21]),
    Request("Shiraki", Role.ICU, 2, [1,2,20,6,13], []),
    Request("Takamoto", Role.ICU, 2, [19,20,28,29,30], []),
    Request("Shimozaki", Role.ER, 2, [4,5,6,13,19], [21,28]),
    Request("Katsu", Role.ER, 0, [26,27,28,20,30], []),
    Request("Matsumoto", Role.ICU, 0, [6,13,3,10,18], []),
    Request("Tamaki", Role.ER, 0, [6,7,14,17,28], []),
    Request("Yuizono", Role.ICU, 2, [12,19,29,7,28], []),
    Request("Kashibuchi", Role.ER, 1, [3,6,15,20,27], [28]),
    Request("Okuno", Role.ER, 0, [13,14,18,24], []),
    Request("Ookura", Role.ER, 0, [21,28,29,30], []),
    Request("Iwakawa", Role.ER, 0, [21], []),
    Request("Takami", Role.ICU, 0, [3,12,19,25], [21, 14, 8, 15, 5, 9]),
    Request("Mitsukuri", Role.ER, 0, [5,6,21], []),
    Request("Oogami", Role.ER, 0, [2,18,19,20,21], [28]),
    Request("Ochi", Role.ER, 0, [6,14,20,27,28], []),
    Request("Takeda", Role.ER, 0, [6,7,27,28,29], []),
    Request("Ono", Role.ER, 0, [7,20,21,27,28], [3,10,17,24]),
    Request("Hasegawa", Role.ER, 0, [18,20,28,29,30], [31]),
    Request("Emoto", Role.ER, 0, [13], []),
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

''' # 任意で指定したければこちら
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

#############################################################################

#############################################################################
# 実行部分
parser = argparse.ArgumentParser()
parser.add_argument('-y', '--year', type=int, default=datetime.datetime.now().year, help='target year: ')
parser.add_argument('-m', '--month', type=int, default=datetime.datetime.now().month, help='target month: ')
parser.add_argument('-a', '--num_sample', type=int, default=5, help='number of printing shift samples')
args = parser.parse_args()

def main():
    target_ym = Target_year_month(year = 2024, month = 7)
    monthly_requests = Convert_to_date(req_list, target_ym.year, target_ym.month)

    intern_count = Intern_counter(monthly_requests)

    # work_counts = Work_count_calculator(target_ym, intern_count, weekday_target_counts, weekend_target_counts)
    work_counts = {
        Role.ICU: {Section.ICU: 17, Section.NER: 3},
        Role.ER: {Section.NER: 6, Section.ER: 6, Section.EICU: 7}
    }

    many_schedules = []
    # 初期シフトをn=20回、その変更をm=5回ずつ模索、合計n*m=100回のシフト作成を行う
    for i in range(30):
        initial_team_schedules = []
        for request in monthly_requests:
            intern_schedule = InternSchedule(request, target_ym)
            intern_schedule.assign_schedule(work_counts)
            initial_team_schedules.append(intern_schedule)
        for j in range(3):
            temp_team_schedules, temp_sec_counts, temp_score, improvement_history = ranking_swap_schedule(initial_team_schedules, weekday_target_counts, weekend_target_counts)
            print(f"\rnow producing schedule samples...{i*2 + j + 1}/100", end="")
            satisfaction_score, satisfaction_stdev = intern_satisfaction_stats(temp_team_schedules)
            trial = f"Trial{i*3 + j + 1}"
            temp = [trial, temp_score, satisfaction_stdev, satisfaction_score, temp_team_schedules, temp_sec_counts]
            many_schedules.append(temp)
    print("")

    # 作成したn*m=100個のシフトから、まずsectionerr=シフト条件充足度の減点、次に研修医間のシフト満足度の偏差をsortして表示
    many_schedules.sort(key=itemgetter(1,2))
    for temp in many_schedules:
        print(f"{temp[0]}...SectionErr: {temp[1]}, Intern_stdev: {temp[2]:.2f}, Intern_sum:{temp[3]}")

    print("================================================")

    # sortしたシフト案を順番にn個表示する
    top_n_schedules = []
    for _ in range(args.num_sample):
        final_team_schedules = many_schedules[_][4]
        final_sec_counts = many_schedules[_][5]
        final = [final_team_schedules, final_sec_counts]
        top_n_schedules.append(final)

    for finals in top_n_schedules:
        final_team_schedules = finals[0]
        final_sec_counts = finals[1]
        for intern in final_team_schedules:
            intern.set_NG_B()
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

main()