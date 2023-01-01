import datetime

import django
import pika
from django.db.models import Q

from cheaters_project.settings import RMQ_QUEUE_NAME, RMQ_HOST

from checker.models import Group, AttemptsCheckJobs, Contest, Attempt, Problem, Participant, Job


def send_tasks_to_check(groups: [Group] = None, contests: [Contest] = None, problems: Problem = None,
                        participants: Participant = None, job: Job = None):
    attempts = None
    if groups:
        attempts = Attempt.objects.filter(
            problem_contest__contest__group__in=groups,
            problem_contest__threshold__isnull=False,
            outcome='accepted'
        ).order_by('alias')
    if contests:
        attempts = Attempt.objects.filter(
            problem_contest__contest__in=contests,
            problem_contest__threshold__isnull=False,
            outcome='accepted'
        ).order_by('alias')
    if problems:
        attempts = Attempt.objects.filter(
            problem_contest__problem__in=problems,
            problem_contest__threshold__isnull=False,
            outcome='accepted'
        ).order_by('alias')
    if participants:
        attempts = Attempt.objects.filter(
            participant__in=participants,
            problem_contest__threshold__isnull=False,
            outcome='accepted'
        )
    return add_jobs(list(attempts), job)


def add_jobs(attempts: [Attempt], job: Job = None):
    RMQ_CONNECTION = pika.BlockingConnection(pika.ConnectionParameters(RMQ_HOST))
    RMQ_CHANNEL = RMQ_CONNECTION.channel()
    RMQ_CHANNEL.queue_declare(queue=RMQ_QUEUE_NAME, durable=True)
    newely_added = 0
    exception_raised = 0
    n = len(attempts)
    for i in range(n):
        for j in range(i + 1, n):
            try:
                if attempts[i].participant.pcms_id != attempts[j].participant.pcms_id and \
                        attempts[i].problem_contest.problem == attempts[j].problem_contest.problem:
                    a_j = AttemptsCheckJobs()
                    a_j.job = job
                    a_j.attempt_lhs = attempts[i]
                    a_j.attempt_rhs = attempts[j]
                    a_j.status = 'NOT_STARTED'
                    a_j.checking_start_time = datetime.datetime.now()
                    a_j.save()
                    newely_added += 1
                    RMQ_CHANNEL.basic_publish(exchange='',
                                              routing_key='checker',
                                              body=f'{a_j.pk}')
            except django.db.utils.IntegrityError:
                exception_raised += 1

    return f'Neweley added = {newely_added}; Exception raised = {exception_raised}, all = {n}'


def mock():
    send_tasks_to_check([Group.objects.last()])
