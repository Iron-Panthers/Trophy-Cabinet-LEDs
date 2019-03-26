import collections
from datetime import datetime, timedelta
from dateutil import tz

Duration = collections.namedtuple('Duration', 'start end')

pdt = tz.tzoffset('PDT', -25200)
now = datetime(year=2019, month=3, day=11, tzinfo=pdt, hour=7, minute=00)
period = timedelta(weeks=1)

monday = [
	# Before 1
	Duration(
		datetime(year=2019, month=3, day=11, tzinfo=pdt, hour=7, minute=00), 
		datetime(year=2019, month=3, day=11, tzinfo=pdt, hour=8, minute=00), 
	),
	# 1-2
	Duration(
		datetime(year=2019, month=3, day=11, tzinfo=pdt, hour=8, minute=50), 
		datetime(year=2019, month=3, day=11, tzinfo=pdt, hour=8, minute=57), 
	),
	# Break
	Duration(
		datetime(year=2019, month=3, day=11, tzinfo=pdt, hour=9, minute=46), 
		datetime(year=2019, month=3, day=11, tzinfo=pdt, hour=9, minute=58)
	),
	# 3-4
	Duration(
		datetime(year=2019, month=3, day=11, tzinfo=pdt, hour=10, minute=52), 
		datetime(year=2019, month=3, day=11, tzinfo=pdt, hour=10, minute=59)
	),
	# Lunch
	Duration(
		datetime(year=2019, month=3, day=11, tzinfo=pdt, hour=11, minute=53), 
		datetime(year=2019, month=3, day=11, tzinfo=pdt, hour=12, minute=30)
	),
	# 5-6
	Duration(
		datetime(year=2019, month=3, day=11, tzinfo=pdt, hour=13, minute=19), 
		datetime(year=2019, month=3, day=11, tzinfo=pdt, hour=13, minute=26)
	),
	# 6-7
	Duration(
		datetime(year=2019, month=3, day=11, tzinfo=pdt, hour=14, minute=15), 
		datetime(year=2019, month=3, day=11, tzinfo=pdt, hour=14, minute=22)
	),
	# After school
	Duration(
		datetime(year=2019, month=3, day=11, tzinfo=pdt, hour=15, minute=11), 
		datetime(year=2019, month=3, day=11, tzinfo=pdt, hour=16, minute=11)
	),
]

wednesday_block = [
	# Before 2
	Duration(
		datetime(year=2019, month=3, day=13, tzinfo=pdt, hour=7, minute=00), 
		datetime(year=2019, month=3, day=13, tzinfo=pdt, hour=9, minute=00)
	),
	# Break
	Duration(
		datetime(year=2019, month=3, day=13, tzinfo=pdt, hour=10, minute=32), 
		datetime(year=2019, month=3, day=13, tzinfo=pdt, hour=10, minute=49)
	),
	# Lunch
	Duration(
		datetime(year=2019, month=3, day=13, tzinfo=pdt, hour=12, minute=20), 
		datetime(year=2019, month=3, day=13, tzinfo=pdt, hour=12, minute=52)
	),
	# office hours, after school
	Duration(
		datetime(year=2019, month=3, day=13, tzinfo=pdt, hour=14, minute=28), 
		datetime(year=2019, month=3, day=13, tzinfo=pdt, hour=16, minute=00)
	),
]

thursday_block = [
	# Before 1
	Duration(
		datetime(year=2019, month=3, day=14, tzinfo=pdt, hour=7, minute=00), 
		datetime(year=2019, month=3, day=14, tzinfo=pdt, hour=8, minute=00)
	),
	# Break
	Duration(
		datetime(year=2019, month=3, day=14, tzinfo=pdt, hour=9, minute=32), 
		datetime(year=2019, month=3, day=14, tzinfo=pdt, hour=9, minute=49)
	),
	# Lunch
	Duration(
		datetime(year=2019, month=3, day=14, tzinfo=pdt, hour=11, minute=20), 
		datetime(year=2019, month=3, day=14, tzinfo=pdt, hour=11, minute=55)
	),
	# 5-7
	Duration(
		datetime(year=2019, month=3, day=14, tzinfo=pdt, hour=13, minute=31), 
		datetime(year=2019, month=3, day=14, tzinfo=pdt, hour=13, minute=40)
	),
	# After school
	Duration(
		datetime(year=2019, month=3, day=14, tzinfo=pdt, hour=15, minute=11), 
		datetime(year=2019, month=3, day=14, tzinfo=pdt, hour=16, minute=00)
	),
]

repeated_tests = [
	Duration(
		datetime(year=2019, month=3, day=14, tzinfo=pdt, hour=7, minute=00, second=0), 
		datetime(year=2019, month=3, day=14, tzinfo=pdt, hour=7, minute=00, second=5)
	),
	Duration(
		datetime(year=2019, month=3, day=14, tzinfo=pdt, hour=7, minute=00, second=10), 
		datetime(year=2019, month=3, day=14, tzinfo=pdt, hour=7, minute=00, second=20)
	),
	Duration(
		datetime(year=2019, month=3, day=14, tzinfo=pdt, hour=7, minute=00, second=25), 
		datetime(year=2019, month=3, day=14, tzinfo=pdt, hour=7, minute=00, second=30)
	),
	Duration(
		datetime(year=2019, month=3, day=14, tzinfo=pdt, hour=7, minute=00, second=40), 
		datetime(year=2019, month=3, day=14, tzinfo=pdt, hour=7, minute=00, second=55)
	),
]

durations = []

for k in [timedelta(0), timedelta(days=1), timedelta(days=4)]:
	durations += [
		Duration(s + k, e + k) for s, e in monday
	]

durations += wednesday_block + thursday_block

durations.sort(key=lambda x: x.start)

output = ','.join(f'LEDDuration{{{int(d.start.timestamp())},{int(d.end.timestamp() - d.start.timestamp())}}}' for d in durations)
output = 'LEDDuration schedule[SCHEDULE_COUNT] = {' + output + '};'

print(f'#define PERIOD {int(period.total_seconds())}')
print(f'#define SCHEDULE_COUNT {len(durations)}')
print(output)
