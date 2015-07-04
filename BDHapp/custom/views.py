from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import user_passes_test

def group_required(*group_names):
    """
    Requires user membership in at least one of the groups passed in.

    Checks is_active and allows superusers to pass regardless of group
    membership.
    """
    def in_group(u):
        return u.is_active and (u.is_superuser or bool(u.groups.filter(name__in=group_names)))
    return user_passes_test(in_group)

from_email = 'ejerzyk@gmail.com'