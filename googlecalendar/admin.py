from django.contrib import admin

from models import Account, Calendar, Event
from forms import AccountForm

class CalendarInline(admin.TabularInline):
    model = Calendar
    extra = 0
    fieldsets = (
            (None,
                {'fields':(
                    'title',
                    'uri',
                    'feed_uri',
                )}
            ),
        )
        
class EventsInline(admin.TabularInline):
    model = Event
    extra = 0
    fieldsets = (
            (None,
                {'fields':(
                    'title',
                    'start_time',
                    'end_time',
                )}
            ),
        )

class AccountAdmin(admin.ModelAdmin):
    form = AccountForm
    inlines = [CalendarInline]

class CalendarAdmin(admin.ModelAdmin):
    list_display = ['title', 'account', 'where']
    list_filter= ['account']
    inlines = [EventsInline]
    fieldsets = (
            (None,
                {'fields':(
                    'title',
                    'summary',
                )}
            ),
            ('URLs',
                {'fields':(
                    'uri',
                    'feed_uri',
                )}
            ),
        )

class EventAdmin(admin.ModelAdmin):
    search_fields = ['title','content']
    date_hierarchy = 'start_time'
    ordering = ['-start_time']
    list_display = ['title', 'start_time', 'end_time']
    list_filter= ['calendar']
    fieldsets = (
            (None,
                {'fields':(
                    'title',
                    'content',
                    ('start_time','end_time'),
                )}
            ),
            ('URLs',
                {'fields':(
                    'uri',
                    'edit_uri',
                    'view_uri',
                )}
            ),
        )

try:
    admin.site.register(Account, AccountAdmin)
    admin.site.register(Calendar, CalendarAdmin)
    admin.site.register(Event, EventAdmin)
except admin.sites.AlreadyRegistered:
    pass