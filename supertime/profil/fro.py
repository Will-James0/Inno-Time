from datetime import datetime, timedelta, timezone,date


da=date.today()
nj=da.monthrange(da.year,da.month)[1]
print(nj)