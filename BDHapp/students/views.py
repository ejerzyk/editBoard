from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from custom.views import group_required

from django.utils.timezone import get_current_timezone

from django.contrib.auth.models import User, Group

# Create your views here.
@login_required
def lookup(request):

	return render(request, 'students/lookup.html', context)

@login_required
@group_required('ssw', 'section_ed', 'edit_board')
def edit(request):
	return render(request, 'students/edit.html', context)