from django.utils.safestring import mark_safe
from django.template import Library
from django.contrib.auth.models import User

import json


register = Library()

@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))

@register.filter(name='lookup')
def lookup(d, key):
	return d[key]

@register.filter(name='group_string')
def group_string(username):
	print username
	user = User.objects.get(username=username)
	group_names = []
	for g in user.groups.all():
		group_names += [translate(g.name)]
	return ', '.join(group_names)

PERMISSION_CHOICES = (
		('CE', 'COPY ED'),
		('SW', 'SENIOR STAFF WRITER'),
		('SE', 'SECTION ED'),
		('EB', 'EDIT BOARD'),
	)

@register.filter(name='translate')
def translate(s):
	translation_obj = {}
	translation_obj['ssw'] = 'Senior Staff Writer'
	translation_obj['section_ed'] = 'Section Editor'
	translation_obj['edit_board'] = 'Editorial Board'
	translation_obj['UN'] = 'University News'
	translation_obj['M'] = 'Metro'
	translation_obj['AC'] = 'Arts & Culture'
	translation_obj['S'] = 'Sports'
	translation_obj['SR'] = 'Science & Research'
	translation_obj['CU'] = 'Create User'
	translation_obj['CP'] = 'Change Permission'
	translation_obj['CE'] = 'Copy Editor'
	translation_obj['SW'] = 'Senior Staff Writer'
	translation_obj['SE'] = 'Section Editor'
	translation_obj['EB'] = 'Edit Board'
	if s in translation_obj:
		return translation_obj[s]
	else:
		return s 

@register.filter(name='format_phone_num')
def format_phone_num(pn):
	if len(pn) == 10:
		area_code = pn[:3]
		first_three = pn[3:6]
		last_four = pn[6:]
		return '(' + area_code + ') ' + first_three + '-' + last_four
	else:
		return pn