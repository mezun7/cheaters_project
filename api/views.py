from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets, permissions

from api.serializers import ParticipantSerializer, ContestSerializer, AttemptSerializer, AttemptsCheckJobsSerializer
from checker.helpers.helpers import get_attempts_checking_jobs_statement, get_attempts_checking_jobs_score_statement
from checker.models import Participant, Contest, Attempt, AttemptsCheckJobs


@login_required
def test(request):
    return render(request, 'checker/test.html')


class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all().order_by('name')
    serializer_class = ParticipantSerializer


class ContestViewSet(viewsets.ModelViewSet):
    queryset = Contest.objects.all().order_by('name')
    serializer_class = ContestSerializer


class AttemptViewSet(viewsets.ModelViewSet):
    queryset = Attempt.objects.all().order_by('alias')
    serializer_class = AttemptSerializer


class AttemptsCheckJobsViewSet(viewsets.ModelViewSet):
    serializer_class = AttemptsCheckJobsSerializer
    permission_classes = [permissions.IsAuthenticated]

    # print(request.user)

    def get_queryset(self):
        queryset = AttemptsCheckJobs.objects.all().order_by('pk')
        return queryset


class CheckingInProgressViewSet(viewsets.ModelViewSet):
    serializer_class = AttemptsCheckJobsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        statement = get_attempts_checking_jobs_statement(self.request, ['NOT_STARTED', 'CHECKING'])
        queryset = AttemptsCheckJobs.objects.filter(statement).distinct().order_by('pk')
        return queryset


class PendingManualCheckViewSet(viewsets.ModelViewSet):
    serializer_class = AttemptsCheckJobsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        statement = get_attempts_checking_jobs_statement(self.request, ['NOT_SEEN'])
        statement_score = get_attempts_checking_jobs_score_statement()
        queryset = AttemptsCheckJobs.objects.filter(statement & statement_score).distinct().order_by('pk')
        return queryset


class ListOfCheatersViewSet(viewsets.ModelViewSet):
    serializer_class = AttemptsCheckJobsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        statement = get_attempts_checking_jobs_statement(self.request, ['CHEATED'])
        queryset = AttemptsCheckJobs.objects.filter(statement).distinct().order_by('-manual_check_time')
        return queryset
