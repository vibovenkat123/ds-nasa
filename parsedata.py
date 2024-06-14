from datetime import datetime, timedelta
from record import Record


def read_until_space(s: str):
    re = ""
    for c in s:
        if c == " ":
            break
        re += c
    return re, s[len(re):].strip()


year = 0
month = 0
day = 0


def parse(txt: str):
    records = []
    global year
    global month
    global day
    # get 45 days before current date
    min_date = datetime.now() - timedelta(days=45)
    for line in txt.splitlines()[2:]:
        year, line = read_until_space(line)
        year = int(year)
        month, line = read_until_space(line)
        month = int(month)
        day, line = read_until_space(line)
        day = int(day)
        temp_d = datetime(year=year, month=month, day=day)
        if temp_d < min_date:
            continue
        hour, line = read_until_space(line)
        hour = int(hour)
        minute, line = read_until_space(line)
        minute = int(minute)
        dat = datetime(year=year, month=month, day=day, hour=hour, minute=minute)
        # wind direction
        wdir, line = read_until_space(line)
        if wdir == "MM":
            wdir = None
        else:
            wdir = float(wdir)
        # speed
        wspeed, line = read_until_space(line)
        if wspeed == "MM":
            wspeed = None
        else:
            wspeed = float(wspeed)

        # records
        rec = Record(dat, wdir, wspeed)
        records.append(rec)

    return records