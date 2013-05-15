import string, random
from datetime import datetime

def timesince(dt, default=None):
	if default is None:
		default = 'Just now'

	now = datetime.utcnow()
	diff = now - dt

	periods = (
		(diff.days / 365, "year", "years"),
		(diff.days / 30, "month", "months"),
		(diff.days / 7, "week", "weeks"),
		(diff.days, "day", "days"),
		(diff.seconds / 3600, "hour", "hours"),
		(diff.seconds / 60, "minute", "minutes"),
		(diff.seconds, "second", "seconds"),
	)

	for period, sinular, plural in periods:

		if not period:
			continue

		if period == 1:
			re = '%d %s ago' % (period, sinular)
		else:
			re = '%d %s ago' % (period, plural)

		return re

	return default

def floorsign(floor=1):
	return 'Floor %d' % floor

def rand_string(length=15):
	return ''.join(random.choice(string.letters + string.digits) for ii in range (length))