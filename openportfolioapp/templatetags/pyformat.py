from django import template
from django.conf import settings

class PyFormatNode(template.Node):
	def __init__(self, variable, format_str):
		self.variable = variable
		self.format_str = format_str

	def render(self, context):
		try:
			var = self.variable.resolve(context)
			format = self.format_str.resolve(context)

			return format . format(var)
		except:
			if settings.TEMPLATE_DEBUG:
				raise
			return ''

def do_pyformat(parser, token):
    tag_name, variable, format_str = token.split_contents()
    return PyFormatNode(parser.compile_filter(variable), 
                        parser.compile_filter(format_str),
                        )

register = template.Library()
register.tag('pyformat', do_pyformat)