# -*- coding: utf-8 -*-

import string, random, re
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

def hash_geo(address):
	a = address.split(',')[:2]
	if len(a) < 2:
		return ''
	a[0] = float(a[0])
	a[1] = float(a[1])
	return '%f,%f' % (a[0]+a[1], a[0]-a[1])

def editor_filter(s):
	rand_hold = "owpmafuaoFerewaHWAFNASDJPAoSDFAQPAN"
	p = re.compile(r'div>', re.I)
	s = p.sub('p>', s)
	s = s.replace('<p>', "\n<p>")
	s = s.replace('http://www.v5snj.com', '')

	p = re.compile(r'<img\ssrc="/static/img/emos/(\d+).gif">')
	s = p.sub(r'owpmafuaoFerewaHWAFNASDJPAoSDFAQPAN\1', s)

	p = re.compile(r'<(.*?)>')
	s = p.sub('', s)
	p = re.compile(r'owpmafuaoFerewaHWAFNASDJPAoSDFAQPAN(\d+)')
	s = p.sub(r'<img src="/static/img/emos/\1.gif">', s)

	p = re.compile(r'^$', re.M)
	s = p.sub('<br>', s)
	s = '<p>' + s.replace("\n", '</p><p>') + '</p>'
	return s