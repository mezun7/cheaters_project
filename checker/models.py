from django.contrib.auth.models import User
from django.db import models

from checker.entities.entities import CONTEST_TYPE_CHOICES, CHECKING_STATUS_CHOICES, OUTCOME_CHOICES, AUTH_TYPE_CHOICES


# Create your models here.

class UserType(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auth_type = models.CharField(max_length=2, choices=AUTH_TYPE_CHOICES)
    login_pcms = models.CharField(max_length=100, null=True, blank=True)
    password_pcms = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        constraints = [models.CheckConstraint(
            name="%(app_label)s_%(class)s If you choose builtin auth, you should enter pcms login and password",
            check=models.Q(auth_type='p') | (models.Q(auth_type='b') &
                                             models.Q(login_pcms__isnull=False) & models.Q(
                        password_pcms__isnull=False))
        )]


class Group(models.Model):
    users_have_access = models.ManyToManyField(User)
    name = models.CharField(max_length=1000)
    login = models.CharField(max_length=1000)
    password = models.CharField(max_length=1000)
    api_url = models.CharField(null=True, blank=True, max_length=1000)


class Problem(models.Model):
    name = models.CharField(max_length=1000)
    pcms_id = models.CharField(max_length=1000)
    last_check_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name


class Contest(models.Model):
    users_have_access = models.ManyToManyField(User)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=1000)
    pcms_id = models.CharField(max_length=1000)
    contest_id = models.CharField(max_length=1000)
    scoring_model = models.CharField(max_length=50, choices=CONTEST_TYPE_CHOICES)
    last_check_time = models.DateTimeField(blank=True, null=True)
    problem = models.ManyToManyField(Problem, through='ContestProblem')
    last_page_downloaded = models.IntegerField(null=True, blank=True)
    last_attempt_id_downloaded = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name


class ContestProblem(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    alias = models.CharField(max_length=30)
    last_check_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.contest}: {self.alias}. {self.problem}'


class Participant(models.Model):
    pcms_id = models.CharField(max_length=1000)
    name = models.CharField(max_length=1000)
    contest = models.ManyToManyField(Contest, null=True, blank=True)

    def __str__(self):
        return self.name


class Attempt(models.Model):
    pcms_id = models.CharField(max_length=1000)
    score = models.IntegerField()
    outcome = models.CharField(max_length=1000, choices=OUTCOME_CHOICES)
    status = models.CharField(max_length=1000, null=True, blank=True)
    participant = models.ForeignKey(Participant, on_delete=models.Model)
    problem_contest = models.ForeignKey(ContestProblem, on_delete=models.Model)
    time = models.IntegerField()
    language = models.CharField(max_length=1000)
    source = models.FileField(upload_to='upload/sources/')

    class Meta:
        ordering = ['time', 'pcms_id']


class Job(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, null=True, blank=True)
    problems = models.ManyToManyField(Problem)
    participant = models.ManyToManyField(Participant)
    groups = models.ManyToManyField(Group)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['end_time', 'start_time']


class AttemptsCheckJobs(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    attempt_lhs = models.ForeignKey(Attempt, on_delete=models.CASCADE, related_name='jobs_lhs')
    attempt_rhs = models.ForeignKey(Attempt, on_delete=models.CASCADE, related_name='jobs_rhs')
    script_checking_result = models.FloatField()
    status = models.CharField(max_length=100, choices=CHECKING_STATUS_CHOICES)
    checking_start_time = models.DateTimeField(null=True, blank=True)
    checking_end_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('attempt_lhs', 'attempt_rhs')


class FileUploadTest(models.Model):
    file = models.FileField(upload_to='upload/sources/')
