import json
import os
import urllib

from django.db.models import Min, Q, F

from cheaters_project import settings
from checker.models import Group, Contest, AttemptsCheckJobs


def get_attempts_checking_jobs_statement(request, statuses):
    statement_lhs = Q(attempt_lhs__problem_contest__contest__group__users_have_access__in=[request.user]) & Q(
        status__in=statuses)
    statement_rhs = Q(
        attempt_rhs__problem_contest__contest__group__users_have_access__in=[request.user]) & Q(status__in=statuses)
    return statement_lhs | statement_rhs


def get_attempts_to_check(request):
    statement = get_attempts_checking_jobs_statement(request, ['NOT_SEEN'])
    statement_score = Q(script_checking_result__lte=F('attempt_lhs__problem_contest__threshold'))

    attempts_to_check = AttemptsCheckJobs.objects.filter(statement & statement_score). \
        distinct().count()

    return attempts_to_check


def get_remaining_attempts_checking_running(request):
    statement = get_attempts_checking_jobs_statement(request, ['NOT_STARTED', 'CHECKING'])
    remaining_attempts_checking_running = AttemptsCheckJobs.objects.filter(statement).distinct().count()
    return remaining_attempts_checking_running


def get_number_of_all_approved_cheaters(request):
    statement = get_attempts_checking_jobs_statement(request, ['CHEATED'])
    all_approved_cheaters = AttemptsCheckJobs.objects.filter(statement).distinct().count()
    return all_approved_cheaters


def get_menu_info(request, page_title):
    groups = Group.objects.filter(users_have_access__in=[request.user])

    last_problems_update_time = Contest.objects.filter(group__users_have_access__in=[request.user]).aggregate(
        Min('last_contest_problems_parsing_time'))['last_contest_problems_parsing_time__min']
    last_attempts_update_time = Contest.objects.filter(group__users_have_access__in=[request.user]).aggregate(
        Min('last_attempt_parsing_time'))['last_attempt_parsing_time__min']
    context = {
        'groups': groups,
        'attempts_to_check': get_attempts_to_check(request),
        'remaining_attempts_checking_running': get_remaining_attempts_checking_running(request),
        'page_title': page_title.capitalize(),
        'all_approved_cheaters': get_number_of_all_approved_cheaters(request),
        'last_problems_update_time': last_problems_update_time,
        'last_attempts_update_time': last_attempts_update_time,
    }
    return context


def get_raw_str(path):
    fl = open(os.path.join(settings.MEDIA_ROOT, path), 'r')
    text = ''.join(fl.readlines())
    return repr(text)


def check_login_password_exists(login: str, password: str, api_url: str) -> bool:
    check_url = api_url + f'client/api/party/contest/list?login={login}&password={password}&format=json'
    with urllib.request.urlopen(check_url) as url:
        json_dictionary = json.loads(url.read().decode())
    # print(json_dictionary, type(json_dictionary))
    return 'ok' in json_dictionary.keys()
