from .staff import Time, Section, target_cal, staffs, print_ng_count
from .monthlyschedules import Monthly_schedules

def main():
    print_ng_count(staffs)
    for i in range(50):
        print(f">>> RUNNING ATTEMPT {i+1}")
        for staff in staffs:
            staff.work_count = 0
            staff.extra_count = 0
            staff.personal_schedule = {date: {Time.day: Section.OFF, Time.night: Section.OFF} for date in target_cal}
            staff.personal_schedule.update({date: {Time.day: Section.NG, Time.night: Section.NG} for date in staff.ng_request})
        monthly_schedules = Monthly_schedules()
        monthly_schedules.assign_30591()
        flag = monthly_schedules.assign_icu_and_eicu()
        if not flag:
            continue
        flag = monthly_schedules.assign_taitou()
        if not flag:
            continue
        monthly_schedules.assign_day_night()
        monthly_schedules.swap_GAIKIN_dummy()
        monthly_schedules.swap_phd()
        monthly_schedules.swap_DAY_NIGHT_dummy()
        break
    monthly_schedules.print_generated_schedules()
    monthly_schedules.print_staff_stats()
    monthly_schedules.find_free_candidates()

if __name__ == "__main__":
    main()
