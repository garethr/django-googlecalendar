#!/usr/bin/env python

from django.core.management.base import BaseCommand

from googlecalendar.models import Account
        
class Command(BaseCommand):
        
    def handle(self, *args, **options):
        g = Account.objects.all()[0]
        g._get_service()
        cals = g.get_own_calendars()
        for cal in cals:
            cal.save()
            events = cal.get_events()
            for event in events:
                event.save()