from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http  import HttpResponse

from custom.views import group_required
from django.contrib.auth import authenticate, login
from django.utils.timezone import get_current_timezone

from django.contrib.auth.models import User, Group
from django.core.mail import send_mail

from accounts.models import BDHuser, author, perm_request, story, author_relationship, editor_relationship
from custom.views import from_email

import re 
from datetime import datetime
import string
import random

# Create your views here.
def my_auth(request):
	print 'in my_auth'
	if request.method == 'POST':
		print 'POST'
		password = request.POST['password']
		username = request.POST['username']
		next = request.POST['next']
		user = authenticate(username=username, password=password)
		print user
		if user is not None:
			if user.is_active:
				login(request, user)
				return home(request)
			else:
				return HttpResponse('DISABLED ACCOUNT')
		else: 
			return HttpResponse('INVALID LOGIN')
	elif request.method == 'GET':
		print 'GET'
		context = {}
		return render(request, 'accounts/login.html', context)

@login_required
def home(request):
	context = {'edit_board' : False, 'section_ed' : False, 'ssw' : False, 'copy_ed' : False}

	edit_board_group = Group.objects.get(name='edit_board')
	section_ed_group = Group.objects.get(name='section_ed')
	ssw_group = Group.objects.get(name='ssw')
	copy_ed_group = Group.objects.get(name='copy_ed')

	user_groups = request.user.groups.all()

	authorP = False

	if (edit_board_group in user_groups):
		context['edit_board'] = True
		authorP = True
	if (section_ed_group in user_groups):
		context['section_ed'] = True
		authorP = True
	if (ssw_group in user_groups):
		context['ssw'] = True
		authorP = True
	if (copy_ed_group in user_groups):
		context['copy_ed'] = True

	if authorP:
		bdhu = BDHuser.objects.get(user=request.user)
		a = author.objects.get(gen_user=bdhu)
		context['author_id'] = a.id

	return render(request, 'accounts/home.html', context)

def new_user(request):
	context = {}
	return render(request, 'accounts/new_user.html', context)

def created_user(request):
	if request.method == 'POST':
		context = {}
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		username = request.POST['username']
		password = request.POST['password']
		email = request.POST['email'].lower()
		phone_number = request.POST['phone_number']
		class_year = request.POST['class_year']

		create_user = True 
		new_user_context = {'message' : ''}
		if User.objects.filter(username=username):
			new_user_context['message'] += 'Usesrname already exists!'
			create_user = False
		if User.objects.filter(email=email):
			new_user_context['message'] += 'Email already in the system! Try changing your password.'
			create_user = False

		if not create_user:
			return render(request, 'accounts/new_user.html' , new_user_context)

		u = User(username=username, password=password, first_name=first_name, last_name=last_name, email=email, is_active=False)
		u.set_password(password)
		u.save()
		bdhu = BDHuser(user=u, phone_number=phone_number, class_year=class_year)
		bdhu.save()

		user_type = request.POST['user_type']
		if (user_type != 'copy_ed'):
			author_url = 'http://browndailyherald.com/author/'
			author_url += request.POST['author_url']
			section = request.POST['section']
			a = author(gen_user=bdhu, author_url=author_url, section=section)
			a.save()
			np = ''
			if user_type == 'ssw':
				np = 'SW'
			elif user_type == 'section_ed':
				np = 'SE'
			else:
				np = 'EB'
		else:
			np = 'CE'
		r = perm_request(by=bdhu, new_permission=np)
		r.save()
		return render(request, 'accounts/created_user.html', context)
	else:
		return HttpResponse('NOT VALID PAGE WITHOUT USER CREATION')

def error(request):
	context = {}
	return render(request, 'accounts/error.html', context)

@login_required
@group_required('edit_board')
def approve(request):
	context = {}
	if request.method == 'GET':
		sort = request.GET.get('sort')
		if sort is not None:
			context['contents'] = perm_request.objects.all().order_by(sort)
		else:
			context['contents'] = perm_request.objects.all()
		return render(request, 'accounts/approve.html', context)
	else:
		if 'approve' in request.POST:
			to_approve = request.POST.getlist('users')
			for username in to_approve:
				print username
				user = User.objects.get(username=username)
				bdhu = BDHuser.objects.get(user=user)
				r = perm_request.objects.get(by=bdhu)
				if r.req == 'CU':
					user.is_active = True
				if r.new_permission == 'CE':
					user.groups.clear()
					user.groups.add(Group.objects.get(name='copy_ed'))
				elif r.new_permission == 'SW':
					user.groups.clear()
					user.groups.add(Group.objects.get(name='ssw'))
				elif r.new_permission == 'SE':
					user.groups.clear()
					user.groups.add(Group.objects.get(name='section_ed'))
				else:
					user.groups.clear()
					user.groups.add(Group.objects.get(name='edit_board'))
				user.save()
				r.delete()
				send_mail('BDH Internal', 'Your account request has been approved!', from_email, [user.email], fail_silently=False)
		else:
			to_deny = request.POST.getlist('users')
			for username in to_deny:
				user = User.objects.get(username=username)
				bdhu = BDHuser.objects.get(user=user)
				r = perm_request.objects.get(by=bdhu)
				r.delete()
				send_mail('BDH Internal', 'Your account request has been denied.', from_email, [user.email], fail_silently=False)
		request.method = 'GET'
		return approve(request)

@login_required
def lookup_users(request): 
	if request.method == "GET":
		context = {}
		context['edit_board'] = Group.objects.get(name='edit_board') in request.user.groups.all()
		bdhusers = BDHuser.objects.all()
		users = []
		for bdhu in bdhusers:
			authorP = True
			a = None
			try:
				a = author.objects.get(gen_user = bdhu)
			except author.DoesNotExist:
				authorP = False
			users += [{'bdhu' : bdhu, 'authorP' : authorP, 'author' : a}]
		context['users'] = users
		return render(request, 'accounts/lookup_users.html', context)
	else:
		for bdhu in BDHuser.objects.filter(class_year__lte=(int(datetime.now().year) - 4)):
			bdhu.user.delete()
		request.method = 'GET'
		return lookup_users(request)

@login_required
def edit_users(request):
	context = {}
	if request.method == 'GET':
		user = request.user
		context['copy_ed'] = Group.objects.get(name='copy_ed') in user.groups.all()
		context['ssw'] = Group.objects.get(name='ssw') in user.groups.all()
		context['section_ed'] = Group.objects.get(name='section_ed') in user.groups.all()
		context['edit_board'] = Group.objects.get(name='edit_board') in user.groups.all()

		context['bdhuser'] = BDHuser.objects.get(user=user)
		a = author.objects.get(gen_user=context['bdhuser'])
		if a is not None:
			context['author'] = True
			context['a'] = a
			context['author_url'] = a.author_url[35:]
		else:
			context['author'] = False
		return render(request, 'accounts/edit_users.html', context)
	else:
		print request.POST
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		password = request.POST['password']
		email = request.POST['email']
		phone_number = request.POST['phone_number']
		class_year = request.POST['class_year']
		user_type = request.POST['user_type']
		u = request.user
		u.first_name = first_name
		u.last_name = last_name
		if (password != ''):
			u.set_password(password)
		u.email = email 
		if Group.objects.get(name=user_type) not in u.groups.all():
			u.groups.add(Group.objects.get(name=user_type))
		bdhu = BDHuser.objects.get(user=u)
		bdhu.phone_number = phone_number
		bdhu.class_year = class_year
		try:
			a = author.objects.get(gen_user=bdhu)
			author_url = request.POST['author_url']
			section = request.POST['section']
			a.author_url = author_url
			a.section = section
			u.save()
			bdhu.save()
			a.save()
		except author.DoesNotExist:
			u.save()
			bdhu.save()
		request.method = 'GET'
		return edit_users(request)

@login_required
@group_required('ssw', 'section_ed', 'edit_board')
def lookup_stories(request):
	context = {}
	if request.method == 'POST':
		bdhu = BDHuser.objects.get(user=request.user)
		edit_board_group = Group.objects.get(name='edit_board')
		section_ed_group = Group.objects.get(name='section_ed')
		user_groups = request.user.groups.all()
		print 'IN POST'
		if (edit_board_group in user_groups) or (section_ed_group in user_groups):
			print 'IN IF'
			a = author.objects.get(gen_user=bdhu)
			print request.POST
			for checkbox in request.POST:
				if checkbox.isnumeric():
					s = story.objects.get(pk=int(checkbox))
					if editor_relationship.objects.filter(story=s, editor=a).count() > 0:
						if 'remove' in request.POST:
							er = editor_relationship.objects.filter(story=s, editor=a)
							er[0].delete()
					else:
						if 'add' in request.POST:
							er = editor_relationship(story=s, editor=a)
							er.save()
		request.method = 'GET'
		return lookup_stories(request)
	else:
		context = {'edit_board' : False, 'section_ed' : False, 'ssw' : False, 'copy_ed' : False}

		edit_board_group = Group.objects.get(name='edit_board')
		section_ed_group = Group.objects.get(name='section_ed')
		ssw_group = Group.objects.get(name='ssw')
		copy_ed_group = Group.objects.get(name='copy_ed')

		user_groups = request.user.groups.all()

		authorP = False

		if (edit_board_group in user_groups):
			context['edit_board'] = True
			authorP = True
		if (section_ed_group in user_groups):
			context['section_ed'] = True
			authorP = True
		if (ssw_group in user_groups):
			context['ssw'] = True
			authorP = True
		if (copy_ed_group in user_groups):
			context['copy_ed'] = True

		if authorP:
			bdhu = BDHuser.objects.get(user=request.user)
			a = author.objects.get(gen_user=bdhu)
			context['author_id'] = a.id

		sort = request.GET.get('sort')
		if sort is not None:
			context['contents'] = story.objects.all().order_by(sort)
		else:
			context['contents'] = story.objects.all()
		return render(request, 'accounts/lookup_stories.html', context)

@login_required
@group_required('ssw', 'section_ed', 'edit_board')
def by_page(request):
	print 'IN BY PAGE'
	context = {}
	author_id = int(request.GET.get('author'))
	a = author.objects.get(pk=author_id)
	context['author'] = a
	if a is not None:
		# a.scrape(True)
		stories = []
		sort = request.GET.get('sort')
		story_ids = author_relationship.objects.filter(author=a).values_list('story', flat=True).order_by('story')
		for story_id in story_ids:
			stories.append(story.objects.get(pk=story_id))
		if sort is not None:
			if sort == 'title':
				stories.sort(key=lambda x: x.title)
			elif sort == 'section':
				stories.sort(key=lambda x: x.section)
			else:
				stories.sort(key=lambda x: x.date)
			print stories
		context['contents'] = stories
		return render(request, 'accounts/by_page.html', context)
	else:
		return HttpResponse('NO AUTHOR SELECTED')

@login_required
@group_required('ssw', 'section_ed', 'edit_board')
def scrape_by_page(request):
	print 'IN SCRAPE_BY_PAGE'
	context = {}
	author_id = int(request.GET.get('author'))
	a = author.objects.get(pk=author_id)
	context['author'] = a
	if a is not None:
		a.scrape(False)
		stories = []
		sort = request.GET.get('sort')
		story_ids = author_relationship.objects.filter(author=a).values_list('story', flat=True).order_by('story')
		for story_id in story_ids:
			stories.append(story.objects.get(pk=story_id))
		if sort is not None:
			if sort == 'title':
				stories.sort(key=lambda x: x.title)
			elif sort == 'section':
				stories.sort(key=lambda x: x.section)
			else:
				stories.sort(key=lambda x: x.date)
			print stories
		context['contents'] = stories
		return render(request, 'accounts/by_page.html', context)
	else:
		return HttpResponse('NO AUTHOR SELECTED')

@login_required
@group_required('section_ed', 'edit_board')
def edit_stories(request):
	return render(request, 'accounts/edit_stories.html', context)

def random_generator(size=10, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))

def reset_password(request):
	context = {}
	context['message'] = ''
	if request.method == 'POST':
		email = request.POST['email'].lower()
		new_password = random_generator()
		try:
		    user = User.objects.get(email=email)
		    user.set_password(new_password)
		    user.save()
		    send_mail('BDH Internal', 'Your password has been changed to ' + new_password, from_email, [email], fail_silently=False)
		    context['message'] = 'Your password has been successfully reset. Please check your email.'
		except User.DoesNotExist:
		    context['message'] = 'This email is not in the system. Please try again.'
	return render(request, 'accounts/reset_password.html', context)







