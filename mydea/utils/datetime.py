"""Utils functions for managing datatime convertions"""

from datetime import datetime

def datetime_str_to_int(date_time_str):
    """Given a date time in string format return 
    a date time in integer format"""

    format_date_time_str = date_time_str.split('+')[0]  # delete UTC  
    return datetime.strptime(format_date_time_str, '%Y-%m-%dT%H:%M:%S.%f').timestamp()