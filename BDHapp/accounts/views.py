from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http  import HttpResponse

from custom.views import group_required
from django.contrib.auth import authenticate, login
from django.utils.timezone import get_current_timezone

from django.contrib.auth.models import User, Group

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

	if (edit_board_group in user_groups):
		context['edit_board'] = True
	if (section_ed_group in user_groups):
		context['section_ed'] = True
	if (ssw_group in user_groups):
		context['ssw'] = True
	if (copy_ed_group in user_groups):
		context['copy_ed'] = True

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
		email = request.POST['email']
		phone_number = request.POST['phone_number']

		user_type = request.POST['user_type']
		if (user_type != 'copy_ed'):
			author_url = request.POST['author_url']
			section = request.POST['section']

		u = User(username=username, password=password, first_name=first_name, last_name=last_name, email=email, is_active=False)
		bdhu = BDHuser(user=u, phone_number=phone_number)

		return render(request, 'accounts/created_user.html', context)
	else:
		return HttpResponse('NOT VALID PAGE WITHOUT USER CREATION')

def error(request):
	return render(request, 'accounts/error.html', context)

@login_required
@group_required('edit_board')
def approve(request):
	return render(request, 'accounts/approve.html', context)

@login_required
def lookup(request):
	return render(request, 'accounts/lookup.html', context)

@login_required
def edit(request):
	return render(request, 'accounts/edit.html', context)