import re
from datetime import datetime

periods = ["minutely"   , "hourly"   , "daily"  , "weekly" , "monthly" , "yearly"]
formats = ["%Y%m%d%H%M" , "%Y%m%d%H" , "%Y%m%d" , "%Y%W"   , "%Y%m"    , "%Y"    ]

DATE                     = 0
SOURCE_IP                = 1
DOMAIN                   = 2
WHITELIST_LOCATION       = 3
RESOLVED_IP              = 4
WHITELIST_LOCATION_NAMES = 5
RECORD_TTYPE             = 6
RESOLVE_STATE            = 7
UNKNOWN_FIELD            = 8
RESOLVE_DETAIL           = 9
UNIQUE_ID                = 10


pattern = re.compile("(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2}).*")
def parse_log_line(line):
    parts = line.split('|')
    full_date = "20" + parts[DATE]
    year, month, day, hour, minute, second = pattern.match(full_date).groups()
    date                     = datetime(int(year), int(month), int(day), \
                                int(hour), int(minute), int(second))
    ip                       = parts[SOURCE_IP]
    domain                   = parts[DOMAIN]
    whitelist_location       = parts[WHITELIST_LOCATION]
    resolved_ips             = filter(lambda x: x is not "", parts[RESOLVED_IP].split(";"))
    whitelist_location_names = parts[WHITELIST_LOCATION_NAMES]
    recod_type               = parts[RECORD_TTYPE]
    resovle_state            = parts[RESOLVE_STATE]
    unknown_field            = parts[UNKNOWN_FIELD]
    resolve_detail           = parts[RESOLVE_DETAIL]
    uniqe_id                 = parts[UNIQUE_ID]

    return (date               , ip            , domain                   , 
            whitelist_location , resolved_ips  , whitelist_location_names , 
            recod_type         , resovle_state , unknown_field            , 
            resolve_detail     , uniqe_id)

def parse_chunk(lines):
    entries = [parse_log_line(line) for line in lines if not line.count("flexi-dns:") and not (line.strip() == "")]
    return entries

def in_whitelist(resolve_detail):
    return resolve_detail[3] == "w"

def get_namelist(resolve_detail):
    if resolve_detail[1] == "B":
        return "B"
    if resolve_detail[2] == "G":
        return "G"
    if resolve_detail[3] == "w":
        return "w"
    else:
        return "-"
        
def is_silent(resolve_detail):
    return get_namelist(resolve_detail) == "-"
