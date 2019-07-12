import datetime

def is_over_days(target_date, limit_days, limit_datetime=None):
  limit_seconds = datetime.timedelta(days=limit_days).total_seconds()
  delta =  (limit_datetime if limit_datetime else datetime.datetime.now(datetime.timezone.utc)) - target_date
  diff_seconds = delta.total_seconds() 

  return diff_seconds >= limit_seconds