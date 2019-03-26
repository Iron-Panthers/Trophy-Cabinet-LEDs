import collections
from datetime import datetime, timedelta
from dateutil import tz

HEADER = '''/* 
 * This is an autogenerated file created at {time}
 * LEDs are on for {leds_on:.2f} hours per cycle.
 * Please do not directly make any changes to this file.
 * The Arduino IDE will not auto-update when this file is changed without it knowing.
 */

#pragma once

#include "LEDDuration.h"
#include "LEDPattern.h"

'''

Duration = collections.namedtuple('Duration', 'start end pattern')

pdt = tz.tzoffset('PDT', -25200)
now = datetime(year=2019, month=3, day=11, tzinfo=pdt, hour=7, minute=00)
period = timedelta(weeks=1)

patterns = {
	'basic': 'new LinearHue(20, 5)',
	'bouncing': 'new BouncingWave(20, 5, 100)',
}

monday = [
	# Before 1
	Duration(
		datetime(year=2019, month=3, day=11, tzinfo=pdt, hour=7, minute=00), 
		datetime(year=2019, month=3, day=11, tzinfo=pdt, hour=8, minute=00), 
		'basic'
	),
	# 1-2
	Duration(
		datetime(year=2019, month=3, day=11, tzinfo=pdt, hour=8, minute=50), 
		datetime(year=2019, month=3, day=11, tzinfo=pdt, hour=8, minute=57), 
		'basic' 
	),
	# Break
	Duration(
		datetime(year=2019, month=3, day=11, tzinfo=pdt, hour=9, minute=46), 
		datetime(year=2019, month=3, day=11, tzinfo=pdt, hour=9, minute=58), 
		'basic'
	),
	# 3-4
	Duration(
		datetime(year=2019, month=3, day=11, tzinfo=pdt, hour=10, minute=52), 
		datetime(year=2019, month=3, day=11, tzinfo=pdt, hour=10, minute=59), 
		'basic'
	),
	# Lunch
	Duration(
		datetime(year=2019, month=3, day=11, tzinfo=pdt, hour=11, minute=53), 
		datetime(year=2019, month=3, day=11, tzinfo=pdt, hour=12, minute=30), 
		'basic'
	),
	# 5-6
	Duration(
		datetime(year=2019, month=3, day=11, tzinfo=pdt, hour=13, minute=19), 
		datetime(year=2019, month=3, day=11, tzinfo=pdt, hour=13, minute=26), 
		'basic'
	),
	# 6-7
	Duration(
		datetime(year=2019, month=3, day=11, tzinfo=pdt, hour=14, minute=15), 
		datetime(year=2019, month=3, day=11, tzinfo=pdt, hour=14, minute=22), 
		'basic'
	),
	# After school
	Duration(
		datetime(year=2019, month=3, day=11, tzinfo=pdt, hour=15, minute=11), 
		datetime(year=2019, month=3, day=11, tzinfo=pdt, hour=16, minute=11), 
		'basic'
	),
]

wednesday_block = [
	# Before 2
	Duration(
		datetime(year=2019, month=3, day=13, tzinfo=pdt, hour=7, minute=00), 
		datetime(year=2019, month=3, day=13, tzinfo=pdt, hour=9, minute=00), 
		'basic'
	),
	# Break
	Duration(
		datetime(year=2019, month=3, day=13, tzinfo=pdt, hour=10, minute=32), 
		datetime(year=2019, month=3, day=13, tzinfo=pdt, hour=10, minute=49), 
		'basic'
	),
	# Lunch
	Duration(
		datetime(year=2019, month=3, day=13, tzinfo=pdt, hour=12, minute=20), 
		datetime(year=2019, month=3, day=13, tzinfo=pdt, hour=12, minute=52), 
		'basic'
	),
	# office hours, after school
	Duration(
		datetime(year=2019, month=3, day=13, tzinfo=pdt, hour=14, minute=28), 
		datetime(year=2019, month=3, day=13, tzinfo=pdt, hour=16, minute=00), 
		'basic'
	),
]

thursday_block = [
	# Before 1
	Duration(
		datetime(year=2019, month=3, day=14, tzinfo=pdt, hour=7, minute=00), 
		datetime(year=2019, month=3, day=14, tzinfo=pdt, hour=8, minute=00), 
		'basic'
	),
	# Break
	Duration(
		datetime(year=2019, month=3, day=14, tzinfo=pdt, hour=9, minute=32), 
		datetime(year=2019, month=3, day=14, tzinfo=pdt, hour=9, minute=49), 
		'basic'
	),
	# Lunch
	Duration(
		datetime(year=2019, month=3, day=14, tzinfo=pdt, hour=11, minute=20), 
		datetime(year=2019, month=3, day=14, tzinfo=pdt, hour=11, minute=55), 
		'basic'
	),
	# 5-7
	Duration(
		datetime(year=2019, month=3, day=14, tzinfo=pdt, hour=13, minute=31), 
		datetime(year=2019, month=3, day=14, tzinfo=pdt, hour=13, minute=40), 
		'basic'
	),
	# After school
	Duration(
		datetime(year=2019, month=3, day=14, tzinfo=pdt, hour=15, minute=11), 
		datetime(year=2019, month=3, day=14, tzinfo=pdt, hour=16, minute=00), 
		'basic'
	),
]

repeated_tests = [
	Duration(
		datetime(year=2019, month=3, day=14, tzinfo=pdt, hour=7, minute=00, second=0), 
		datetime(year=2019, month=3, day=14, tzinfo=pdt, hour=7, minute=00, second=5), 
		'basic'
	),
	Duration(
		datetime(year=2019, month=3, day=14, tzinfo=pdt, hour=7, minute=00, second=10), 
		datetime(year=2019, month=3, day=14, tzinfo=pdt, hour=7, minute=00, second=20), 
		'basic'
	),
	Duration(
		datetime(year=2019, month=3, day=14, tzinfo=pdt, hour=7, minute=00, second=25), 
		datetime(year=2019, month=3, day=14, tzinfo=pdt, hour=7, minute=00, second=30), 
		'basic'
	),
	Duration(
		datetime(year=2019, month=3, day=14, tzinfo=pdt, hour=7, minute=00, second=40), 
		datetime(year=2019, month=3, day=14, tzinfo=pdt, hour=7, minute=00, second=55), 
		'basic'
	),
]

durations = []

for k in [timedelta(0), timedelta(days=1), timedelta(days=4)]:
	durations += [
		Duration(s + k, e + k, p) for s, e, p in monday
	]

durations += wednesday_block + thursday_block

durations.sort(key=lambda x: x.start)

array = ',\n  '.join(f'LEDDuration{{{int(d.start.timestamp())}, {int(d.end.timestamp() - d.start.timestamp())}, PTRN_{d.pattern}}}' for d in durations)
array = 'LEDDuration schedule[SCHEDULE_COUNT] = {\n  ' + array + '\n};'
count = len(durations)

total_duration = sum(d.end.timestamp() - d.start.timestamp() for d in durations)

with open('trophy_cabinet/schedule.h', 'w') as f:
	f.write(HEADER.format(time=datetime.now(), leds_on=total_duration / 3600))
	f.write(f'#define PERIOD {int(period.total_seconds())}\n')
	f.write(f'#define SCHEDULE_COUNT {count}\n\n')

	for k, v in patterns.items():
		f.write(f'LEDPattern* PTRN_{k} = {v};\n')

	f.write('\n')
	f.write(array)
	f.write('\n')

print(f"Successfully wrote {count} entries to trophy_cabinet/schedule.h")
print(f"LED is on for {total_duration} seconds ({total_duration / 3600} hours) every cycle")
