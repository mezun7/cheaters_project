from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from checker.helpers.helpers import get_menu_info
from checker.models import Group, Contest
from checker.tasks import start_cheaters_checking_job


@login_required
def start_group_checking_view(request):
    pass


@login_required
def start_contests_checking_view(request):
    pass


@login_required
def start_problems_checking_view(request):
    pass


@login_required()
def check_contest(request, contest_id):
    contests = list(Contest.objects.filter(pk=contest_id, group__users_have_access__in=[request.user]).values('pk'))
    atask = start_cheaters_checking_job.delay(contests=contests)
    return HttpResponseRedirect(request.GET['from'] if 'from' in request.GET.keys() else reverse('checker:my_groups'))


@login_required()
def check_group(request, group_id):
    groups = list(Group.objects.filter(users_have_access__in=[request.user], pk=group_id).values('pk'))
    atask = start_cheaters_checking_job.delay(groups=groups)
    return HttpResponseRedirect(request.GET['from'] if 'from' in request.GET.keys() else reverse('checker:my_groups'))


@login_required()
def check_my_groups(request):
    groups = list(Group.objects.filter(users_have_access__in=[request.user]).values('pk'))
    atask = start_cheaters_checking_job.delay(groups=groups)
    return HttpResponseRedirect(reverse('checker:my_groups'))


@login_required()
def checking_in_progress(request):
    context = get_menu_info(request, 'Запущенные проверки')
    return render(request, 'checker/checkings_in_progress.html', context)
