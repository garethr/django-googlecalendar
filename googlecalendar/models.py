import datetime

from django import forms
from django.db import models
from django.contrib import admin

import gdata.service
import gdata.calendar.service

from managers import CalendarManager, EventManager

_services = {}

class Account(models.Model):
	email = models.CharField(max_length = 100)
	password = models.CharField(max_length = 100)
	def __unicode__(self):
	    return u'%s' % self.email
	
	def _get_service(self):
		if not _services.has_key(self.email):
			_service = gdata.calendar.service.CalendarService()
			#_service.source = 'ITSLtd-Django_Google-%s' % VERSION
			_service.email = self.email
			_service.password = self.password
			_service.ProgrammaticLogin()
			_services[self.email] = _service
		return _services[self.email]
	service = property(_get_service, None)
	
	def get_own_calendars(self):
		cals = self.service.GetOwnCalendarsFeed()
		result = []
		for i, cal in enumerate(cals.entry):
			result.append(Calendar.objects.get_or_create(self, cal))
		return result

class Calendar(models.Model):
	objects = CalendarManager()
	account = models.ForeignKey(Account)
	uri = models.CharField(max_length = 255, unique = True)
	title = models.CharField(max_length = 100)
	where = models.CharField(max_length = 100, blank = True)
	timezone = models.CharField(max_length = 100, blank = True)
	summary = models.TextField()
	feed_uri = models.CharField(max_length = 255, blank = True)
	def __unicode__(self):
		return self.title
	def get_events(self):
		events = self.account.service.GetCalendarEventFeed(uri = self.feed_uri)
		result = []
		for i, event in enumerate(events.entry):
			result.append(Event.objects.get_or_create(self, event))
		return result

class Event(models.Model):
	objects = EventManager()
	uri = models.CharField(max_length = 255, unique = True)
	calendar = models.ForeignKey(Calendar)
	title = models.CharField(max_length = 255)
	edit_uri = models.CharField(max_length = 255)
	view_uri = models.CharField(max_length = 255)
	content = models.TextField(blank = True)
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	where = models.CharField(max_length = 255)
	def __unicode__(self):
		return u'%s' % (self.title)
