import re
from datetime import datetime

periods = ["minutely",			"hourly",     	"daily",	"weekly",	"monthly",	"yearly"]
formats = ["%Y%m%d%H%M",	"%Y%m%d%H",	"%Y%m%d",	"%Y%W",	"%Y%m", 	"%Y"    ]

DATE                     = 0
SOURCE_IP                = 1
DOMAIN                   = 2
WHITELIST_LOCATION       = 3
RESOLVED_IP              = 4
WHITELIST_LOCATION_NAMES = 5
DNS_RECORD_TTYPE         = 6
RESOLVE_STATE            = 7
UNKNOWN_FIELD            = 8
RESOLVE_DETAIL           = 9
UNIQUE_ID                = 10


def parse_log_line(line):
    parts = line.split('|')
    year, month, day, hour, minute, second = re.match("(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2}).*", "20" + parts[DATE]).groups()
    date                     = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
    ip                       = parts[SOURCE_IP]
    domain                   = parts[DOMAIN]
    whitelist_location       = parts[WHITELIST_LOCATION]
    resovled_ip              = parts[RESOLVED_IP]
    whitelist_location_names = parts[WHITELIST_LOCATION_NAMES]
    recod_type               = parts[DNS_RECORD_TTYPE]
    resovle_state            = parts[RESOLVE_STATE]
    unknown_field            = parts[UNKNOWN_FIELD]
    resolve_detail           = parts[RESOLVE_DETAIL]
    uniqe_id                 = parts[UNIQUE_ID]
    return (date, ip, domain, whitelist_location, resovled_ip, whitelist_location_names, recod_type, resovle_state, unknown_field,  resolve_detail, uniqe_id)

def parse_chunk(contents):
    entries = [parse_log_line(line) for line in contents.splitlines() if not line.count("flexi-dns:")]
    return entries
