from django.db.models import Manager

from utils import parse_date_w3dtf

class CalendarManager(Manager):
    def get_or_create(self, account, data):
        uri = data.id.text
        try:
            result = self.get(uri = uri)
        except self.model.DoesNotExist:
            result = self.model(account = account)
        result.uri = uri
        for prop in ['summary', 'timezone', 'title', 'where']:
            attr = getattr(data, prop)
            if hasattr(attr, 'text'):
                setattr(result, prop, attr.text or '')
        for link in data.link:
            if link.rel == 'alternate':
                result.feed_uri = link.href
        return result

class EventManager(Manager):
    def get_or_create(self, calendar, data):
        uri = data.id.text
        try:
            result = self.get(uri = uri)
        except self.model.DoesNotExist:
            result = self.model(calendar = calendar)
            result.uri = uri
        result.title = data.title.text or ''
        result.content = data.content.text or ''

        try:
            result.start_time = parse_date_w3dtf(data.when[0].start_time)
            result.end_time = parse_date_w3dtf(data.when[0].end_time)
        except:
            pass

        result.edit_uri = data.GetEditLink().href
        result.view_uri = data.GetHtmlLink().href
        return result