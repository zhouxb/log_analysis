import re
from datetime import datetime

periods = ["minutely",			"hourly",     	"daily",	"weekly",	"monthly",	"yearly"]
formats = ["%y-%m-%d %H:%M",	"%y-%m-%d %H",	"%y-%m-%d",	"%y-%W",	"%y-%m", 	"%y"    ]

DATE                    = 0
SOURCE_IP               = 1
DOMAIN                  = 2
WHITELIST_LOCATION      = 3
RESOLVED_IP             = 4
WHITELIST_LOCATION_NAME = 5
DNS_RECORD_TTYPE        = 6
RESOLVE_DETAIL          = 7
QUERY_RESULT            = 8
UNIQUE_ID               = 9


def parse_log_line(line):
    parts = line.split('|')
    year, month, day, hour, minute, second = re.match("(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2}).*", "20" + parts[0]).groups()
    date                      = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
    ip                        = parts[SOURCE_IP]
    domain                    = parts[DOMAIN]
    whitelist_location        = parts[WHITELIST_LOCATION]
    resovled_ip               = parts[RESOLVED_IP]
    whitelist_location_name   = parts[WHITELIST_LOCATION_NAME]
    recod_type                = parts[DNS_RECORD_TTYPE]
    resolve_detail            = parts[RESOLVE_DETAIL]
    query_result              = parts[QUERY_RESULT]
    uniqe_id                  = parts[UNIQUE_ID]
    return (date, ip, domain, whitelist_location, resovled_ip, whitelist_location_name, recod_type, resolve_detail, query_result, uniqe_id)

def parse_chunk(contents):
    entries = [parse_log_line(line) for line in contents.splitlines() if not line.count("flexi-dns:")]
    return entries
