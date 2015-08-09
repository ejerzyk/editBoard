from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from custom.views import group_required

from django.utils.timezone import get_current_timezone
from django.contrib.auth.models import User, Group
from dateutil.parser import parse 

from accounts.models import author, BDHuser, author_relationship, story, SECTION_CHOICES, editor_relationship

def get_authors_from_group_name(group_name):
	g = Group.objects.get(name=group_name)
	users = g.user_set.all()
	to_return = []
	for u in users:
		bdhu = BDHuser.objects.get(user=u)
		to_return.append(author.objects.get(gen_user=bdhu))
	return to_return

@login_required
@group_required('ssw', 'section_ed', 'edit_board')
def select(request):
	context = {"upper_perms" : False}
	user_groups = request.user.groups.all()
	edit_board_group = Group.objects.get(name='edit_board')
	section_ed_group = Group.objects.get(name='section_ed')
	if edit_board_group in user_groups or section_ed_group in user_groups:
		context['upper_perms'] = True

	context['semester_begin'] = "Jan. 27, 2015"
	context['ssws'] = get_authors_from_group_name('ssw')
	context['ses'] = get_authors_from_group_name('section_ed')
	context['ebs'] = get_authors_from_group_name('edit_board')
	return render(request, 'management/select.html', context)

def generate_total_num_stories(user, start_date, end_date, context):
	if context['total_num_stories']:
		story_ids = author_relationship.objects.filter(author=user).values_list('story', flat=True).order_by('story')
		total_num_stories = 0
		for story_id in story_ids:
			s = story.objects.get(pk=story_id)
			if start_date.date() < s.date < end_date.date():
				total_num_stories += 1
		return total_num_stories
	else:
		return None
def generate_stories_per_week(user, start_date, end_date, context):
	if context['stories_per_week']:
		num_weeks = float((end_date - start_date).days) / float(7)
		story_ids = author_relationship.objects.filter(author=user).values_list('story', flat=True).order_by('story')
		total_num_stories = 0
		for story_id in story_ids:
			s = story.objects.get(pk=story_id)
			if start_date.date() < s.date < end_date.date():
				total_num_stories += 1
		return float(total_num_stories) / float(num_weeks)
	else:
		return None
def generate_stories_per_section(user, start_date, end_date, context):
	if context['stories_per_section']:
		story_ids = author_relationship.objects.filter(author=user).values_list('story', flat=True).order_by('story')
		section_data = {}
		for story_id in story_ids:
			s = story.objects.get(pk=story_id)
			if start_date.date() < s.date < end_date.date():
				if s.section not in section_data:
					section_data[s.section] = 1
				else: 
					section_data[s.section] += 1
		return section_data
	else:
		return None
def generate_primary_stories_per_week(user, start_date, end_date, context):
	if context['primary_stories_per_week']:
		section = 'university news'
		for tup in SECTION_CHOICES:
			if user.section == tup[0]:
				section = tup[1].lower()
				break

		num_weeks = float((end_date - start_date).days) / float(7)

		story_ids = author_relationship.objects.filter(author=user).values_list('story', flat=True).order_by('story')
		num_primary_stories = 0
		for story_id in story_ids:
			s = story.objects.get(pk=story_id)
			if start_date.date() < s.date < end_date.date():
				if section in s.section.lower():
					num_primary_stories += 1
		return float(num_primary_stories) / float(num_weeks)
def generate_edited_stories_per_week(user, start_date, end_date, context):
	if context['edited_stories_per_week']:
		num_weeks = float((end_date - start_date).days) / float(7)

		story_ids = editor_relationship.objects.filter(editor=user).values_list('story', flat=True).order_by('story')
		num_stories = 0
		for story_id in story_ids:
			s = story.objects.get(pk=story_id)
			if start_date.date() < s.date < end_date.date():
				num_stories += 1
		return float(num_stories) / float(num_weeks)
	else:
		return None
def generate_percent_edited_for_section(user, start_date, end_date, context):
	if context['percent_edited_for_section']:
		section = 'university news'
		for tup in SECTION_CHOICES:
			if user.section == tup[0]:
				section = tup[1].lower()
				break

		edited_story_ids = editor_relationship.objects.filter(editor=user).values_list('story', flat=True).order_by('story')
		total_story_ids = story.objects.filter(section__icontains=section)
		print edited_story_ids
		print total_story_ids

		edited_stories = 0
		total_stories = 0
		for es in edited_story_ids:
			s = story.objects.get(pk=es)
			if (start_date.date() < s.date < end_date.date()) and (section in s.section.lower()):
				edited_stories += 1
		for ts in total_story_ids:
			if start_date.date() < ts.date < end_date.date():
				total_stories += 1
		print edited_stories
		print total_stories
		return (float(edited_stories) / float(total_stories)) * 100
	else:
		return None
def generate_report_data(user, scrapeP, start_date, end_date, context):
	if scrapeP:
		user.scrape(True)

	return {'total_num_stories' : generate_total_num_stories(user, start_date, end_date, context), 'stories_per_week': generate_stories_per_week(user, start_date, end_date, context), 'stories_per_section': generate_stories_per_section(user, start_date, end_date, context), 'primary_stories_per_week' : generate_primary_stories_per_week(user, start_date, end_date, context), 'edited_stories_per_week' : generate_edited_stories_per_week(user, start_date, end_date, context), 'percent_edited_for_section' : generate_percent_edited_for_section(user, start_date, end_date, context)}


@login_required
@group_required('ssw', 'section_ed', 'edit_board')
def report(request):
	if request.method == 'POST':
		context = {'total_num_stories': False, 'stories_per_week': False, 'stories_per_section': False, 'primary_stories_per_week': False, 'edited_stories_per_week' : False, 'percent_edited_for_section' : False}
		users = []
		scrapeP = False
		for checkbox in request.POST:
			print checkbox
			if checkbox.isnumeric():
				users += [author.objects.get(id=int(checkbox))]
			elif checkbox == 'scrape':
				print checkbox
				scrapeP = True
			elif checkbox != 'ssw' and checkbox != 'section_ed' and checkbox != 'edit_board':
				context[checkbox] = True
		print scrapeP
		start_date = parse(request.POST['when_start'])
		end_date = parse(request.POST['when_end'])
		content = {}
		for user in users:
			content[user] = generate_report_data(user, scrapeP, start_date, end_date, context)
		context['data_to_display'] = content
		return render(request, 'management/report.html', context)
	else:
		return HttpResponse("INVALID PAGE WITH NO SELECTION")