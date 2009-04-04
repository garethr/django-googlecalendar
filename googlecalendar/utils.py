import re
import time
import datetime
import gdata.calendar.service

def parse_date_w3dtf(dateString):
	def __extract_date(m):
		year = int(m.group('year'))
		if year < 100:
			year = 100 * int(time.gmtime()[0] / 100) + int(year)
		if year < 1000:
			return 0, 0, 0
		julian = m.group('julian')
		if julian:
			julian = int(julian)
			month = julian / 30 + 1
			day = julian % 30 + 1
			jday = None
			while jday != julian:
				t = time.mktime((year, month, day, 0, 0, 0, 0, 0, 0))
				jday = time.gmtime(t)[-2]
				diff = abs(jday - julian)
				if jday > julian:
					if diff < day:
						day = day - diff
					else:
						month = month - 1
						day = 31
				elif jday < julian:
					if day + diff < 28:
					   day = day + diff
					else:
						month = month + 1
			return year, month, day
		month = m.group('month')
		day = 1
		if month is None:
			month = 1
		else:
			month = int(month)
			day = m.group('day')
			if day:
				day = int(day)
			else:
				day = 1
		return year, month, day
	def __extract_time(m):
		if not m:
			return 0, 0, 0
		hours = m.group('hours')
		if not hours:
			return 0, 0, 0
		hours = int(hours)
		minutes = int(m.group('minutes'))
		seconds = m.group('seconds')
		if seconds:
			seconds = int(float(seconds))
		else:
			seconds = 0
		return hours, minutes, seconds
	def __extract_tzd(m):
		'''Return the Time Zone Designator as an offset in seconds from UTC.'''
		if not m:
			return 0
		tzd = m.group('tzd')
		if not tzd:
			return 0
		if tzd == 'Z':
			return 0
		hours = int(m.group('tzdhours'))
		minutes = m.group('tzdminutes')
		if minutes:
			minutes = int(minutes)
		else:
			minutes = 0
		offset = (hours*60 + minutes)
		if tzd[0] == '+':
			return -offset
		return offset
	__date_re = ('(?P<year>\d\d\d\d)'
				 '(?:(?P<dsep>-|)'
				 '(?:(?P<julian>\d\d\d)'
				 '|(?P<month>\d\d)(?:(?P=dsep)(?P<day>\d\d))?))?')
	__tzd_re = '(?P<tzd>[-+](?P<tzdhours>\d\d)(?::?(?P<tzdminutes>\d\d))|Z)'
	__tzd_rx = re.compile(__tzd_re)
	__time_re = ('(?P<hours>\d\d)(?P<tsep>:|)(?P<minutes>\d\d)'
				 '(?:(?P=tsep)(?P<seconds>\d\d(?:[.,]\d+)?))?'
				 + __tzd_re)
	__datetime_re = '%s(?:T%s)?' % (__date_re, __time_re)
	__datetime_rx = re.compile(__datetime_re)
	m = __datetime_rx.match(dateString)
	if (m is None) or (m.group() != dateString): return
	gmt = __extract_date(m) + __extract_time(m)
	if gmt[0] == 0: return
	return datetime.datetime(tzinfo = None, *gmt) + datetime.timedelta(minutes = __extract_tzd(m))

def request_single_token(uri, secure = False, session = True):
	'''
	Call this to get an authorization link
	(will be redirected back to uri provided with 'token' in request.GET)
	'''
	service = gdata.calendar.service.CalendarService()
	scope = 'http://www.google.com/calendar/feeds/'
	return service.GenerateAuthSubURL(uri, scope, secure, session)

def upgrade_token(token):
	'''
	Upgrade a token obtained by request_single_token to a session token
	usable in the Account model
	'''
	service = gdata.calendar.service.CalendarService()
	service.auth_token = token
	service.UpgradeToSessionToken()
	return service.auth_token

def list_cals(account):
	cals = account.get_own_calendars()
	for c in cals:
		print c
		print '--- EVENTS:'
		for e in c.get_events():
			print e

