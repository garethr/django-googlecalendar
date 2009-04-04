from django.db.models import get_model
from django.template import Library, Node, TemplateSyntaxError, resolve_variable
from google.utils import request_single_token

register = Library()

class GoogleCalendarAuthNode(Node):
	def __init__(self, uri):
		self.uri = uri
	def render(self, context):
		uri = resolve_variable(self.uri, context)
		return request_single_token(uri)

def do_google_calendar_auth(parser, token):
	bits = token.contents.split()
	len_bits = len(bits)
	if len_bits != 2:
		raise TemplateSyntaxError('%s tag requires URI as an argument' % bits[0])
	return GoogleCalendarAuthNode(bits[1])

register.tag('google_calendar_auth', do_google_calendar_auth)
