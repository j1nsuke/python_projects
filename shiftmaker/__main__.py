import argparse
import datetime
from operator import itemgetter
from lib import *
from internschedule import InternSchedule
from evaluator import calc_daily_section_counts, intern_satisfaction_stats
from modifier import ranking_swap_schedule

#　変数部分
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
parser.add_argument('-a', '--num_sample', type=int, default=3, help='number of printing shift samples')
args = parser.parse_args()

def main():
    target_ym = Target_year_month(year = args.year, month = args.month)
    monthly_requests = Convert_to_date(req_list, target_ym.year, target_ym.month)

    intern_count = Intern_counter(monthly_requests)

    work_counts = Work_count_calculator(target_ym, intern_count, weekday_target_counts, weekend_target_counts)

    many_schedules = []
    # 初期シフトをn=20回、その変更をm=5回ずつ模索、合計n*m=100回のシフト作成を行う
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