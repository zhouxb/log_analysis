import datetime
def round_num_by(n):
    def inner(a):
        return (a / n) * n
    return inner

def round_minutes_by(n):
    round_num_by_n = round_num_by(n)
    def inner(date):
        return datetime.datetime(date.year, date.month, date.day, date.hour, round_num_by_n(date.minute))
    return inner
