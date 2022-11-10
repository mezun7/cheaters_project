import json
import urllib
from urllib.parse import urljoin
import posixpath
from checker.models import Group, Contest, Participant, Attempt, ContestProblem
from checker.parser.contest_parser import parse_all_contests
from checker.parser.get_api_url import get_api_url
from cheaters_project import settings
import os
import base64


def get_participant(pcms_id: str, name: str, contest: Contest = None) -> Participant:
    try:
        participant = Participant.objects.get(pcms_id=pcms_id)
    except Participant.DoesNotExist:
        participant = Participant()

    participant.pcms_id = pcms_id
    participant.name = name
    participant.save()
    participant.contest.add(contest)
    return participant


def get_specified_attempts(login: str, password: str, contest: Contest, count, from_page):
    api_url = get_api_url()
    attempts_tepmlate_url = f'client/api/admin/run/list?login={login}&password={password}&' \
                            f'contest={contest.contest_id}&count={count}&from={from_page}' \
                            '&detail=source&format=json'
    contest_url = api_url + attempts_tepmlate_url
    with urllib.request.urlopen(contest_url) as url:
        json_dictionary = json.loads(url.read().decode())
    if 'ok' in json_dictionary.keys():
        return json_dictionary
    return None


def get_problem_contest(alias: str, name: str, contest: Contest, login, password):
    try:
        return ContestProblem.objects.get(alias=alias, problem__name=name, contest=contest)
    except ContestProblem.DoesNotExist:
        # TODO start parsing contests
        print('aaaa')
        return None


def get_source_path(participant: Participant, contest: Contest, json_source, job_id):
    path = os.path.join(settings.MEDIA_ROOT, settings.SOURCE_FILES_SAVE_PATH, participant.pcms_id)
    if not os.path.exists(path):
        os.makedirs(path)
    extension = json_source['name'].split('.')[-1]
    name = job_id.split('.')[-5:]
    name = '-'.join(name)
    filename = f'{name}.{extension}'
    path = os.path.join(path, filename)
    fl = open(path, 'w')
    code = json_source['bytes'][37:]
    code = str(base64.b64decode(code), 'utf-8')
    fl.write(code)
    fl.close()
    save_path = posixpath.join(settings.SOURCE_FILES_SAVE_PATH, participant.pcms_id, filename)
    return save_path


def parse_contest_attempts(login: str, password: str, contest: Contest, count=50):
    # try:
    first_attempt_in_chunk = None
    from_page = 0
    stop = False
    if contest.last_attempt_id_downloaded is None:
        count = 100000
        print(count)
    while not stop:
        json_dictionary = get_specified_attempts(login, password, contest, count, from_page)
        if json_dictionary is None:
            break
        if from_page == 0:
            first_attempt_in_chunk = json_dictionary['ok']['item'][0]['job-id']
        if count == 100000:
            stop = True
        # print(json_dictionary)
        for attempt_json in json_dictionary['ok']['item']:
            run_pcms_id = attempt_json['job-id']
            if contest.last_attempt_id_downloaded == run_pcms_id:
                stop = True
                break
            try:
                attempt_db = Attempt.objects.get(pcms_id=run_pcms_id)
            except Attempt.DoesNotExist:
                attempt_db = Attempt()
            participant = get_participant(attempt_json['session'][0]['party-alias'],
                                          attempt_json['session'][0]['party-name'], contest)
            print(f'Processing {participant} with job-id {run_pcms_id}')
            attempt_db.pcms_id = run_pcms_id
            attempt_db.score = int(attempt_json['score'])
            attempt_db.outcome = attempt_json['outcome'].split()[0]
            attempt_db.language = attempt_json['language-id']
            attempt_db.time = int(attempt_json['time'])
            attempt_db.participant = participant
            attempt_db.problem_contest = get_problem_contest(attempt_json['problem'][0]['alias'],
                                                             attempt_json['problem'][0]['name'],
                                                             contest, login, password)
            attempt_db.source = get_source_path(participant, contest,
                                                attempt_json['source-file'][0], run_pcms_id)
            attempt_db.save()
        from_page += 1

    contest.last_attempt_id_downloaded = first_attempt_in_chunk
    contest.save()
    print('Successfully finished')
