import json
import urllib
from datetime import datetime

from django.contrib.auth.models import User
from checker.models import Group

from checker.models import Contest, Problem, ContestProblem
from checker.parser.get_api_url import get_api_url


def get_contest_api_url(login, password):
    contest_template_url = 'client/api/admin/problems?login=%s&password=%s&format=json'
    api_url = get_api_url()
    contest_url = api_url + (contest_template_url % (login, password))

    return contest_url


def get_scoring_model(model_str: str):
    model_str = model_str.split('#')
    return model_str[-1].lower()


def parse_all_contests():
    groups = Group.objects.all()
    for group in groups:
        parse_all_of_group_contests(group)


def parse_all_of_group_contests(group: Group):
    login = group.login
    password = group.password
    contest_url = get_contest_api_url(login, password)
    # try:
    with urllib.request.urlopen(contest_url) as url:
        json_dictionary = json.loads(url.read().decode())
    if 'ok' in json_dictionary.keys():
        print('ok')
        update_contest_data(json_dictionary, group)


def update_contest_data(json_dictionary, group: Group):
    results = json_dictionary['ok']['result']
    contests = json_dictionary['ok']['contest']
    for ind, result in enumerate(results):
        try:
            contest = Contest.objects.get(contest_id=contests[ind]['contest-id'])
            print('Updating', contests[ind]['contest-id'])
        except Contest.DoesNotExist:
            contest = Contest()
            print('Creating', contests[ind]['contest-id'])

        contest.pcms_id = result['id']
        contest.contest_id = contests[ind]['contest-id']
        contest.name = contests[ind]['contest-name']
        contest.scoring_model = get_scoring_model(results[ind]['scoring-model'])
        contest.group = contest.group if group is None else group
        contest.save()

        parse_problems(result['problems'], contest)


def parse_problems(problems, contest):
    for problem in problems:
        try:
            problem_db = Problem.objects.get(pcms_id=problem['id'])
        except Problem.DoesNotExist:
            problem_db = Problem()
        problem_db.pcms_id = problem['id']
        problem_db.name = problem['name']
        problem_db.save()

        try:
            contest_problem = ContestProblem.objects.get(problem=problem_db, contest=contest)
        except ContestProblem.DoesNotExist:
            contest_problem = ContestProblem()

        contest_problem.problem = problem_db
        contest_problem.contest = contest
        contest_problem.alias = problem['alias']

        contest_problem.save()
        contest.last_contest_problems_parsing_time = datetime.now()
