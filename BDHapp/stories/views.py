from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from custom.views import group_required
from django.utils.timezone import get_current_timezone
from django.contrib.auth.models import User, Group
from models import story
from accounts.models import author

# Create your views here.
@login_required
@group_required('ssw', 'section_ed', 'edit_board')
def lookup(request):
	context = {}
	if request.method == 'POST':
		return render(request, 'stories/lookup.html', context)
	else:
		sort = request.GET.get('sort')
		if sort is not None:
			context['contents'] = story.objects.all().order_by(sort)
		else:
			context['contents'] = story.objects.all()
		return render(request, 'stories/lookup.html', context)

@login_required
@group_required('ssw', 'section_ed', 'edit_board')
def by_page(request):
	context = {}
	a = request.GET.get('author')
	context['author'] = a
	if a is not None:
		a = author.objects.get(id=a)
		contents = []
		stories = []
		sort = request.GET.get('sort')
		if sort is not None:
			stories = story.objects.all().order_by(sort)
		else:
			stories = story.objects.all()
		for s in stories:
			if a in s.authors():
				contents.append(s)
		context['contents'] = contents
		return render(request, 'stories/by_page.html', context)
	else:
		return HttpResponse('NO AUTHOR SELECTED')

@login_required
@group_required('section_ed', 'edit_board')
def edit(request):

	return render(request, 'stories/edit.html', context)

@login_required
@group_required('edit_board')
def scrape(request):
	
	return render(request, 'stories/scrape.html', context)