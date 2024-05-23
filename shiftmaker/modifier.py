import random
from collections import defaultdict
from copy import deepcopy
from lib import Section
from evaluator import calc_daily_section_counts

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