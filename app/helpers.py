# -*- coding: utf-8 -*-

import string, random
from datetime import datetime

def timesince(dt, default=None):
	if default is None:
		default = u'刚刚'

	now = datetime.utcnow()
	diff = now - dt

	periods = (
		(diff.days / 365, u'年'),
		(diff.days / 30, u'个月'),
		(diff.days / 7, u'个星期'),
		(diff.days, u'天'),
		(diff.seconds / 3600, u'小时'),
		(diff.seconds / 60, u'分钟'),
		(diff.seconds, u'秒'),
	)

	for period, sinular in periods:

		if not period:
			continue

		return u'%d%s前' % (period, sinular)

	return default

def floorsign(floor=1):
	return u'%d楼的朋友' % floor

def rand_string(length=15):
	return ''.join(random.choice(string.letters + string.digits) for ii in range (length))