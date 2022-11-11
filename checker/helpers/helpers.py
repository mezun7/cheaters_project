import os

from django.db.models import Min

from cheaters_project import settings
from checker.models import Group, Contest


def get_menu_info(request, page_title):
    groups = Group.objects.filter(users_have_access__in=[request.user])
    attempts_to_check = -100
    remaining_attempts_checking_running = -1
    all_approved_cheaters = -1
    last_problems_update_time = Contest.objects.filter(group__users_have_access__in=[request.user]).aggregate(
        Min('last_contest_problems_parsing_time'))['last_contest_problems_parsing_time__min']
    last_attempts_update_time = Contest.objects.filter(group__users_have_access__in=[request.user]).aggregate(
        Min('last_attempt_parsing_time'))['last_attempt_parsing_time__min']
    context = {
        'groups': groups,
        'attempts_to_check': attempts_to_check,
        'remaining_attempts_checking_running': remaining_attempts_checking_running,
        'page_title': page_title.capitalize(),
        'all_approved_cheaters': all_approved_cheaters,
        'last_problems_update_time': last_problems_update_time,
        'last_attempts_update_time': last_attempts_update_time,
    }
    return context


def get_raw_str(path):
    fl = open(os.path.join(settings.MEDIA_ROOT, path), 'r')
    text = ''.join(fl.readlines())
    return repr(text)
