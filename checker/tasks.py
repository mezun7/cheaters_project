from celery import shared_task
from django.contrib.auth.models import User

from checker.checker_mod.checking import send_tasks_to_check
from checker.models import Group, Job, Contest
from checker.parser.attempts_parser import parse_all_group_contest, parse_contest_attempts
from checker.parser.contest_parser import parse_all_of_group_contests


@shared_task
def add(x, y):
    return x + y


@shared_task
def delayed_parse_group(group_id):
    print("parse group started")
    group = Group.objects.get(pk=group_id)
    parse_all_of_group_contests(group)
    # parse_all_group_contest(group)

@shared_task
def delayed_parse_group_contest_attempts(group_id, contest_id):
    print("parse contest attempts started")
    group = Group.objects.get(pk=group_id)
    contest = Contest.objects.get(pk=contest_id)
    parse_contest_attempts(group, contest)


@shared_task()
def start_cheaters_checking_job(groups=None, contests=None, problems=None, participants=None, user_pk=None):
    print(groups)
    job = Job()
    if user_pk:
        user_pk = User.objects.get(pk=user_pk)
    job.user = user_pk
    job.save()
    if groups:
        grps = []
        for group in groups:
            try:
                tmp_grp = Group.objects.get(pk=group['pk'])
                grps.append(tmp_grp)

            except Group.DoesNotExist:
                print(f'Group with pk - {group["pk"]} doesn\'t exists.')
        job.groups.add(*grps)
        return send_tasks_to_check(groups=grps, job=job)
    elif contests:
        cntsts = []
        for contest in contests:
            try:
                tmp_cnts = Contest.objects.get(pk=contest['pk'])
                cntsts.append(tmp_cnts)
            except Contest.DoesNotExist:
                print(f'Contests with pk - {contest["pk"]} doesn\'t exists.')

        job.contest.add(*cntsts)
        return send_tasks_to_check(contests=cntsts, job=job)
    elif problems:
        prblms = []
        for problem in problems:
            try:
                tmp_cnts = Contest.objects.get(pk=problem['pk'])
                prblms.append(tmp_cnts)
            except Contest.DoesNotExist:
                print(f'Contests with pk - {problem["pk"]} doesn\'t exists.')
        job.contest.add(*prblms)
        return send_tasks_to_check(contests=prblms, job=job)
    elif participants:
        parties = []
        for participant in participants:
            try:
                tmp_cnts = Contest.objects.get(pk=participant['pk'])
                parties.append(tmp_cnts)
            except Contest.DoesNotExist:
                print(f'Contests with pk - {participant["pk"]} doesn\'t exists.')
        job.contest.add(*parties)
        return send_tasks_to_check(contests=parties, job=job)
