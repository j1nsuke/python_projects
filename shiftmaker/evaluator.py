import statistics
from collections import defaultdict
from lib import Section

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
            score += shortage if section in (Section.EICU, Section.ICU, Section.ER) else shortage*3
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
