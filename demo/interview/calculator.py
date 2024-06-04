"""
    :Date: 2024-5-28
    :Author: linshukai
    :Description: About Time calculator(时间计算器)
"""


def calculate_time(start_time, duration):
    st_list = start_time.split()
    st_begin = st_list[0]
    st_end = st_list[1]

    st_hour, st_minute = st_begin.split(":")
    d_hour, d_minute = duration.split(":")

    if not st_hour.isdigit() or not st_minute.isdigit():
        return

    if not d_hour.isdigit() or not d_minute.isdigit():
        return

    if st_end == "PM":
        st_hour = int(st_hour) + 12

    days = 0
    next_hour = 0
    minutes = int(st_minute) + int(d_minute)
    if minutes >= 60:
        next_hour += 1
        minutes %= 60

    hours = int(st_hour) + int(d_hour) + next_hour
    if hours >= 24:
        days = hours // 24
        hours %= 24

    res_time = ""
    minutes = str(minutes) if minutes > 10 else f"0{minutes}"
    if hours >= 12:
        res_time = str(hours % 12) + ":" + minutes + " " + "PM"
    else:
        hours = str(hours) if hours != 0 else "12"
        res_time = hours + ":" + minutes + " " + "AM"
    return res_time, days


def add_time(start, duration, weekend=""):
    new_time, days = calculate_time(start, duration)

    if weekend != "":
        weekend_list = [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        ]
        weekend = weekend.lower()
        if weekend not in weekend_list:
            return

        weekend_index = weekend_list.index(weekend)
        next_weekend_index = (weekend_index + days) % 7
        weekend = weekend_list[next_weekend_index]
        new_time += ", " + weekend.title()

    days_suffix = ""
    if days > 0:
        days_suffix = f"({days} days later)" if days > 1 else "(next day)"
        new_time += " " + days_suffix

    return new_time


if __name__ == "__main__":
    print(add_time("3:30 PM", "2:12"))
    print(add_time("11:55 AM", "3:12"))
    print(add_time("2:59 AM", "24:00"))
    print(add_time("2:59 AM", "24:00", "saturDay"))
    print(add_time("11:59 PM", "24:05", "Wednesday"))
