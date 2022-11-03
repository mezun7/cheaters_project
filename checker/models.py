from django.db import models

from checker.entities.entities import CONTEST_TYPE_CHOICES


# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=1000)
    login = models.CharField(max_length=1000)
    password = models.CharField(max_length=1000)
    api_url = models.CharField(null=True, blank=True, max_length=1000)


class Problem(models.Model):
    name = models.CharField(max_length=1000)
    pcms_id = models.CharField(max_length=1000)
    last_check_time = models.DateTimeField(blank=True, null=True)


class Contest(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=1000)
    pcms_id = models.CharField(max_length=1000)
    contest_id = models.CharField(max_length=1000)
    scoring_model = models.CharField(max_length=10, choices=CONTEST_TYPE_CHOICES)
    last_check_time = models.DateTimeField(blank=True, null=True)
    problem = models.ManyToManyField(Problem, through='ContestProblem')


class ContestProblem(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    alias = models.CharField(max_length=30)
    last_check_time = models.DateTimeField(null=True, blank=True)


class Participant(models.Model):
    pcms_id = models.CharField(max_length=1000)
    name = models.CharField(max_length=1000)


class Attempt(models.Model):
    pcms_id = models.CharField(max_length=1000)
    score = models.IntegerField()
    outcome = models.CharField(max_length=1000)
    status = models.CharField(max_length=1000)
    participant = models.ForeignKey(Participant, on_delete=models.Model)
    problem_contest = models.ForeignKey(ContestProblem, on_delete=models.Model)
    time = models.IntegerField()
    language = models.CharField(max_length=1000)


class Jobs(models.Model):
    attempt_lhs = models.ForeignKey(Attempt, on_delete=models.CASCADE, related_name='jobs_lhs')
    attempt_rhs = models.ForeignKey(Attempt, on_delete=models.CASCADE, related_name='jobs_rhs')
    script_checking_result = models.FloatField()
    status = models.CharField(max_length=100)
    checking_start_time = models.DateTimeField(null=True, blank=True)
    checking_end_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('attempt_lhs', 'attempt_rhs')
