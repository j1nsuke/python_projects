import random
day_list = [day for day in range(1,31)]
for _ in range(15):
    request_days = random.sample(day_list, 4)
    response_days = random.sample(day_list, 6)
    print(f"    Request(\"Dr{_+1}\", Role.ER, {random.randint(0,2)}, {request_days}, {response_days}),")
for _ in range(5):
    request_days = random.sample(day_list, 4)
    response_days = random.sample(day_list, 6)
    print(f"    Request(\"Dr{_+16}\", Role.ICU, {random.randint(0,2)}, {request_days}, {response_days}),")


# Request("Dr20", Role.ICU, 1, [20], [1, 2, 5])