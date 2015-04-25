import pytz
import dateutil
from datetime import datetime
import geonames

# return timezone of geolocation using geonames API
def get_timezone(ll):
    lat = ll.split(',')[0]
    lon = ll.split(',')[1]
    geonames_client = geonames.GeonamesClient('smartviz')
    geonames_result = geonames_client.find_timezone({'lat': lat, 'lng': lon})
    tz_id = geonames_result['timezoneId']
    return pytz.timezone(tz_id)

# Get start of day from request date and add timezone
def get_datetz(date_str, ll):
    if not date_str: return None
    if date_str:
        dd = datetime.strptime(date_str,'%Y-%m-%d')
        date = datetime(dd.year, dd.month, dd.day)
        tz = get_timezone(ll)
        return tz.localize(date)

# return datetime of today based on geolocation
def get_today(ll):
    lat = ll.split(',')[0]
    lon = ll.split(',')[1]
    geonames_client = geonames.GeonamesClient('smartviz')
    geonames_result = geonames_client.find_timezone({'lat': lat, 'lng': lon})
    tz_id = geonames_result['timezoneId']
    now_str = geonames_result['time']
    tz = pytz.timezone(tz_id)
    dd = dateutil.parser.parse(now_str)
    today = datetime(dd.year,dd.month,dd.day)
    return tz.localize(today)
