from django.contrib.auth.models import User
from django.db import models

from checker.entities.entities import CONTEST_TYPE_CHOICES, CHECKING_STATUS_CHOICES, OUTCOME_CHOICES, AUTH_TYPE_CHOICES


# Create your models here.

# class UserType(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     auth_type = models.CharField(max_length=2, choices=AUTH_TYPE_CHOICES)
#     login_pcms = models.CharField(max_length=100, null=True, blank=True)
#     password_pcms = models.CharField(max_length=100, null=True, blank=True)
#
#     def __str__(self):
#         return self.user.username
#
#     class Meta:
#         constraints = [models.CheckConstraint(
#             name="%(app_label)s_%(class)s If you choose builtin auth, you should enter pcms login and password",
#             check=models.Q(auth_type='p') | (models.Q(auth_type='b') &
#                                              models.Q(login_pcms__isnull=False) & models.Q(
#                         password_pcms__isnull=False))
#         )]


class Group(models.Model):
    users_have_access = models.ManyToManyField(User)
    name = models.CharField(max_length=1000)
    login = models.CharField(max_length=1000)
    password = models.CharField(max_length=1000)
    api_url = models.CharField(null=True, blank=True, max_length=1000)

    class Meta:
        unique_together = ('login', 'password', 'api_url')

    def save(self, *args, **kwargs):
        from checker.tasks import delayed_parse_group
        super(Group, self).save(*args, **kwargs)
        delayed_parse_group.delay(self.pk)

    def __str__(self):
        return self.name


class Problem(models.Model):
    name = models.CharField(max_length=1000)
    pcms_id = models.CharField(max_length=1000)
    last_check_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name


class Contest(models.Model):
    users_have_access = models.ManyToManyField(User)
    group = models.ManyToManyField(Group, blank=True)
    name = models.CharField(max_length=1000)
    pcms_id = models.CharField(max_length=1000)
    contest_id = models.CharField(max_length=1000)
    scoring_model = models.CharField(max_length=50, choices=CONTEST_TYPE_CHOICES)
    last_check_time = models.DateTimeField(blank=True, null=True)
    problem = models.ManyToManyField(Problem, through='ContestProblem')
    last_page_downloaded = models.IntegerField(null=True, blank=True)
    last_attempt_id_downloaded = models.CharField(max_length=1000, null=True, blank=True)
    last_attempt_parsing_time = models.DateTimeField(auto_now_add=True)
    last_contest_problems_parsing_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ContestProblem(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    alias = models.CharField(max_length=30)
    last_check_time = models.DateTimeField(null=True, blank=True)
    threshold = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'{self.contest.name}: {self.alias}. {self.problem.name}'


class Participant(models.Model):
    pcms_id = models.CharField(max_length=1000)
    name = models.CharField(max_length=1000)
    contest = models.ManyToManyField(Contest, blank=True)

    def __str__(self):
        return self.name


class Attempt(models.Model):
    pcms_id = models.CharField(max_length=1000)
    alias = models.IntegerField(null=True)
    score = models.IntegerField()
    outcome = models.CharField(max_length=1000, choices=OUTCOME_CHOICES)
    status = models.CharField(max_length=1000, null=True, blank=True)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    problem_contest = models.ForeignKey(ContestProblem, on_delete=models.CASCADE)
    time = models.BigIntegerField()
    language = models.CharField(max_length=1000)
    source = models.FileField(upload_to='upload/sources/')

    def __str__(self):
        return f'{self.participant.name}, {self.alias}, PRB: {self.problem_contest.problem.name}'

    class Meta:
        ordering = ['alias', 'time', 'pcms_id']
        unique_together = ('pcms_id',)


class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    contest = models.ManyToManyField(Contest, blank=True)
    problems = models.ManyToManyField(Problem, blank=True)
    participant = models.ManyToManyField(Participant, blank=True)
    groups = models.ManyToManyField(Group, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['end_time', 'start_time']


class AttemptsCheckJobs(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True)
    rmq_job_id = models.CharField(max_length=200, null=True, blank=True)
    attempt_lhs = models.ForeignKey(Attempt, on_delete=models.CASCADE, related_name='jobs_lhs')
    attempt_rhs = models.ForeignKey(Attempt, on_delete=models.CASCADE, related_name='jobs_rhs')
    script_checking_result = models.FloatField(null=True)
    status = models.CharField(max_length=100, choices=CHECKING_STATUS_CHOICES)
    checking_start_time = models.DateTimeField(null=True, blank=True)
    checking_end_time = models.DateTimeField(null=True, blank=True)
    manual_check_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('attempt_lhs', 'attempt_rhs')
        ordering = ['pk']
