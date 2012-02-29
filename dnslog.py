import re
from datetime import datetime
def parse_log_entry(line):
    parts = line.split('|')
    year, month, day, hour, minute, second = re.match("(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2}).*", "20" + parts[0]).groups()
    return (datetime(int(year), int(month), int(day), int(hour), int(minute), int(second)), parts[1], parts[2])
