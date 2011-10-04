import locale

from django import template 
#from django import assignment_tag

register = template.Library()

from django.template import Variable, VariableDoesNotExist
@register.filter
def hash(object, attr):
	pseudo_context = { 'object' : object }
	try:
		value = Variable('object.%s' % attr).resolve(pseudo_context)
	except VariableDoesNotExist:
		value = None
	return value


@register.filter
def currency(value, arg = '', symbol = True):
    '''
    Currency formatting template filter.

    Takes a number -- integer, float, decimal -- and formats it according to
    the locale specified as the template tag argument (arg). Examples:

      * {{ value|currency }}
      * {{ value|currency:"en_US" }}
      * {{ value|currency:"pt_BR" }}
      * {{ value|currency:"pt_BR.UTF8" }}

    If the argument is omitted, the default system locale will be used.

    The third parameter, symbol, controls whether the currency symbol will be
    printed or not. Defaults to true.

    As advised by the Django documentation, this template won't raise
    exceptions caused by wrong types or invalid locale arguments. It will
    return an empty string instead.

    Be aware that currency formatting is not possible using the 'C' locale.
    This function will fall back to 'en_US.UTF8' in this case.
    '''

    saved = '.'.join([x for x in locale.getlocale() if x]) or (None, None)
    given = arg and ('.' in arg and str(arg) or str(arg) + '.UTF-8')

    # Workaround for Python bug 1699853 and other possibly related bugs.
    if '.' in saved and saved.split('.')[1].lower() in ('utf', 'utf8'):
        saved = saved.split('.')[0] + '.UTF-8'

    if saved == (None, None) and given == '':
        given = 'en_US.UTF-8'

    try:
        locale.setlocale(locale.LC_ALL, given)

        return locale.currency(value or 0, symbol, True)

    except (TypeError, locale.Error):
        return ''

    finally:
        locale.setlocale(locale.LC_ALL, saved)


@register.filter
def formatdata(value,formattype,formatarg=''):
	
	if formattype=='':
		return value
		
	if formattype=='percentage':
		return percentage(value)
		


@register.filter
def percentage(value):
	
	if value=='' or value is None:
		return ''
	
	return '{0:.2%}'.format(value)


def callMethod(obj, methodName):
	method = getattr(obj, methodName)

	if obj.__dict__.has_key("__callArg"):
		ret = method(*obj.__callArg)

		del obj.__callArg
		return ret

	return method()

def args(obj, arg):
	if not obj.__dict__.has_key("__callArg"):
		obj.__callArg = []

	obj.__callArg += [arg]
	return obj

register.filter("call", callMethod)
register.filter("args", args)

class DataFrameXSNode(template.Node):
	def __init__(self, df, idx,var_name):
		self.df = df
		self.idx = idx
		self.var_name = var_name

	def render(self, context):
		context[self.var_name] = context[self.df].xs(context[self.idx])
		return ''

import re
@register.tag
def dataframe_xs(parser, token):
  	# This version uses a regular expression to parse tag contents.
	try:
		# Splitting by None == splitting by spaces.
		tag_name, arg = token.contents.split(None, 1)
		
	except ValueError:
		raise template.TemplateSyntaxError("%r tag requires arguments" % token.contents.split()[0])
	m = re.search(r'(.*?),(.*?) as (\w+)', arg)

	if not m:
		raise template.TemplateSyntaxError("%r tag had invalid arguments" % tag_name)
	df,idx,var_name = m.groups()
	# if not (format_string[0] == format_string[-1] and format_string[0] in ('"', "'")):
	#         raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
	return DataFrameXSNode(df, idx,var_name)


class DataFrameSum(template.Node):
	def __init__(self, df, col,var_name):
		self.df = df
		self.col = col
		self.var_name=var_name

	def render(self, context):
		
		context[self.var_name]=context[self.df][self.col].sum()
		return ''

import re
@register.tag
def dataframe_sum(parser, token):
  	# This version uses a regular expression to parse tag contents.
	try:
		# Splitting by None == splitting by spaces.
		tag_name, arg = token.contents.split(None, 1)
	

	except ValueError:
		raise template.TemplateSyntaxError("%r tag requires arguments" % token.contents.split()[0])
	
	m = re.search(r'(.*?),(.*?) as (\w+)', arg)

	if not m:
		raise template.TemplateSyntaxError("%r tag had invalid arguments" % tag_name)
	df,col,var_name = m.groups()


	# if not (format_string[0] == format_string[-1] and format_string[0] in ('"', "'")):
	#         raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
	return DataFrameSum(df,col,var_name)