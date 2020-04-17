import re
from datetime import datetime
from dateutil.relativedelta import relativedelta

units = [
    {
        'main_string': 'seconds',
        'alt_strings': ['s', 'sec', 'secs', 'second', 'seconds']
    },
    {
        'main_string': 'minutes',
        'alt_strings': ['m', 'min', 'mins', 'minute', 'minutes']
    },
    {
        'main_string': 'hours',
        'alt_strings': ['h', 'hr', 'hrs', 'hour', 'hours']
    },
    {
        'main_string': 'days',
        'alt_strings': ['d', 'day', 'days']
    },
    {
        'main_string': 'weeks',
        'alt_strings': ['w', 'wk', 'wks', 'week', 'weeks']
    },
    {
        'main_string': 'months',
        'alt_strings': ['mn', 'mon', 'mons', 'month', 'months']
    },
    {
        'main_string': 'years',
        'alt_strings': ['y', 'yr', 'yrs', 'year', 'years']
    }
]

def get_time_string(time):
    string = ''
    for unit, amount in time_to_dict(time).items():
        if amount == 0:
            continue
        if amount == 1:
            unit = unit[:-1]
        string += f'{str(amount)} {unit}, '
    string = string[:-2]
    return string

def get_datetime(time):
    return datetime.utcnow() + relativedelta(**time_to_dict(time))

def time_to_dict(time):
    time_dict = {
        'years': 0,
        'months': 0,
        'weeks': 0,
        'days': 0,
        'hours': 0,
        'minutes': 0,
        'seconds': 0
    }
    for (amount, alt) in re.findall(r'([0-9]+)\s*([A-Za-z]+)', time):
        unit = next(u for u in units if alt.lower() in u['alt_strings'])
        if unit:
            time_dict[unit['main_string']] = int(amount)
    return time_dict