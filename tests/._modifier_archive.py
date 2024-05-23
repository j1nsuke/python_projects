'''# divergent_search() とにかくassign_schedule()を繰り返してスコアを改善させる手法
def divergent_search(team_schedules, weekday_target_counts, weekend_target_counts, initial_temperature=10, iterations=2000):
    temperature = initial_temperature
    improvements = []

    init_sec_counts, init_scores = calc_daily_section_counts(team_schedules, weekday_target_counts, weekend_target_counts)

    for i in range(iterations):
        new_team_schedules = copy.deepcopy(team_schedules)

        random_intern_index = random.randint(0, len(new_team_schedules) - 1)
        new_intern = new_team_schedules[random_intern_index]
        new_intern.assign_schedule()

        new_sec_counts, new_scores = calc_daily_section_counts(new_team_schedules, weekday_target_counts, weekend_target_counts)
        
        # 改善度した場合ログに残す
        improvement = init_scores - new_scores
        if improvement > 0:
            improvements.append(improvement)
        else:
            improvements.append('')

        # 改善があれば、スケジュールを更新
        if improvement > 0:
            temperature = initial_temperature
            team_schedules = new_team_schedules
            best_team_schedules = team_schedules # こちらのメソッドでのみ、best_team_schedulesを更新する
            init_scores = new_scores
            init_sec_counts = new_sec_counts
        
        else:
            # 続けて改善がない場合には複数一気に入れ替える
            temperature *= 0.9
            if random.random() > temperature:
                dices = []
                i = random.randint(1, 10)
                for _ in range(i):
                    dices.append(random.randint(0, len(new_team_schedules) - 1))
                random_interns = []
                for dice in dices:
                    random_interns.append(new_team_schedules[dice])
                for intern in random_interns:
                    intern.assign_schedule()

                new_sec_counts, new_scores = calc_daily_section_counts(new_team_schedules, weekday_target_counts, weekend_target_counts)

                improvement = init_scores - new_scores
                improvements.append(improvement)

                team_schedules = new_team_schedules
                init_scores = new_scores
                init_sec_counts = new_sec_counts
    
    best_sec_counts, best_scores = calc_daily_section_counts(best_team_schedules, weekday_target_counts, weekend_target_counts)

    return best_team_schedules, best_sec_counts, best_scores, improvements

initial_team_schedules, final_sec_counts, final_score, improvement_history = divergent_search(initial_team_schedules, weekday_target_counts, weekend_target_counts)
'''
'''# shortage_swap_schedule() daily_section_countsのshortageからランダムに入れ替えるべき勤務を見つける手法
def swap_schedule(team_schedules, weekday_target_counts, weekend_target_counts, iterations=1000):
    improvements = []

    for i in range(iterations):
        shortage_date = None
        shortage_section = None

        init_sec_counts, init_scores = calc_daily_section_counts(team_schedules, weekday_target_counts, weekend_target_counts)

        for date, section_counts in init_sec_counts.items():
            weekday = date.weekday()
            target_counts = weekday_target_counts if weekday < 5 else weekend_target_counts  # 平日と週末で目標人数を切り替える
            sections = [section for section, count in section_counts.items() if count > 0]
            if len(sections) > 0:
                date_unfound = False
                shortage_section = random.choice(sections)
                shortage_date = date
                print(f"\r{shortage_date}: {shortage_section}")
        
        for intern in team_schedules:
            if intern.schedule[shortage_date] == Section.OFF:
                swap_dates = [date for date, section in intern.schedule.items() if section == shortage_section]
                if swap_dates:
                    swap_date = random.choice(swap_dates)
                    intern.schedule[shortage_date] = shortage_section
                    intern.schedule[swap_date] = Section.OFF
                    break
            else:
                continue
            break
                
        valid = all(intern.is_valid() for intern in team_schedules)
        if not valid:
            continue

        new_sec_counts, new_scores = calc_daily_section_counts(team_schedules, weekday_target_counts, weekend_target_counts)
        improvement = init_scores - new_scores
        improvements.append(improvement)

    best_sec_counts, best_scores = calc_daily_section_counts(team_schedules, weekday_target_counts, weekend_target_counts)

    return team_schedules, best_sec_counts, best_scores, improvements

# swap_schedule()の実行
final_team_schedules, final_sec_counts, final_score, improvement_history = swap_schedule(initial_team_schedules, weekday_target_counts, weekend_target_counts)
'''
''' evaluatorの0埋めは結局しないほうがよかったっぽい
def calc_daily_section_counts(team_schedules, weekday_target_counts, weekend_target_counts):
    daily_section_counts = defaultdict(lambda: defaultdict(int))
    daily_section_diffs = defaultdict(lambda: defaultdict(int))
    
    # 0埋めしたほうが多分均一になる
    start_date = team_schedules[0].datelist[0]
    end_date = team_schedules[0].datelist[-1]
    for date in (start_date + datetime.timedelta(days=n) for n in range((end_date - start_date).days + 1)):
        for section in [Section.ICU, Section.ER, Section.NER, Section.EICU]:
            daily_section_counts[date][section] = 0
    
    
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