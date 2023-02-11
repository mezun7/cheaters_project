from django.contrib.auth.decorators import login_required
from django.db.models import Min, Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls import reverse

from checker.forms import GroupAddForm
from checker.helpers.helpers import get_menu_info
from checker.models import Job, Group, Contest
from checker.tasks import delayed_parse_group


# Create your views here.
@login_required()
def main(request):
    context = get_menu_info(request, 'Main')

    return render(request, 'checker/index.html', context=context)


def login_auth(request):
    pass


@login_required()
def group(request, group_id: int):
    group = Group.objects.get(pk=group_id)
    context = get_menu_info(request, group.name)
    contests = Contest.objects.filter(group__in=[group])
    context['contests'] = contests
    context['group'] = group
    return render(request, 'checker/group.html', context=context)


@login_required()
def add_group(request):
    if request.method == 'POST':
        form = GroupAddForm(request.POST)
        if form.is_valid():
            grp = form.save()
            grp.users_have_access.add(request.user)
        else:
            print('Form is not valid', form)

    return HttpResponseRedirect(reverse('checker:my_groups'))


@login_required()
def edit_group(request, group_id: int):
    context = get_menu_info(request, 'Edit_group')
    return render(request, 'checker/index.html', context=context)


@login_required()
def contest(request, contest_id: int):
    context = get_menu_info(request, 'Contest')
    return render(request, 'checker/groups.html', context=context)


@login_required()
def pending_manual_check(request):
    context = get_menu_info(request, 'Pending manual check')
    return render(request, 'checker/pending_manual_check.html', context=context)


@login_required()
def automatic_checking(request):
    context = get_menu_info(request, 'Automatic checking')
    return render(request, 'checker/index.html', context=context)


@login_required()
def all_cheaters(request):
    context = get_menu_info(request, "All cheaters")
    return render(request, 'checker/list_of_cheaters.html', context=context)


@login_required()
def remove_group(request, group_id):
    try:
        gr = Group.objects.get(pk=group_id)
        gr.delete()
    except Group.DoesNotExist:
        print(f'Group with id {group_id} doesnt exists.')
    return HttpResponseRedirect(reverse('checker:my_groups'))


@login_required()
def my_groups(request):
    context = get_menu_info(request, 'Мои группы')
    addGroupForm = GroupAddForm()
    myGroups = Group.objects. \
        filter(users_have_access__in=[request.user]). \
        values('pk', 'name', 'login', 'password', 'api_url').annotate(
            last_contest_problems_parsing_time=Min('contest__last_contest_problems_parsing_time'),
            last_attempt_parsing_time=Min('contest__last_attempt_parsing_time'), num_of_contests=Count('contest__name'),
            last_check_time=Min('contest__last_check_time'))
    context['my_groups'] = myGroups
    context['addGroupForm'] = addGroupForm
    return render(request, 'checker/groups.html', context)


@login_required()
def start_sync(request, group_id):
    # grp = Group.objects.get(pk=group_id)
    delayed_parse_group.delay(group_id)
    return HttpResponseRedirect(reverse('checker:group', kwargs={'group_id': group_id}))


@login_required()
def sync_contest(request, group_id, contest_id):
    delayed_parse_group.delay(group_id)
    return HttpResponseRedirect(reverse('checker:group', kwargs={'group_id': group_id}))
