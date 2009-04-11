#!/usr/bin/env python

from django.core.management.base import BaseCommand
from django.conf import settings

from googlecalendar.models import Account
        
class Command(BaseCommand):
        
    def handle(self, *args, **options):
        accounts = Account.all()
        for account in accounts:
            account._get_service()
            cals = account.get_own_calendars()
                
            for cal in cals:
                if cal.title in settings.CALENDAR_NAMES:
                    print "saving %s" % cal
                    cal.save()
                    events = cal.get_events()
                    for event in events:
                        print "saving %s" % event
                        event.save()
                else:
                    print "ignoring %s" % cal