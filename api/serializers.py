from django.contrib.auth.models import User
from rest_framework import serializers

from checker.models import AttemptsCheckJobs, Participant, Attempt, Group, Contest, Job, ContestProblem, Problem


class ParticipantSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Participant
        fields = (
            'id', 'name', 'pcms_id'
        )


class GroupSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Group
        fields = (
            'id', 'name', 'login', 'password'
        )


class ContestSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Contest
        fields = (
            'id', 'name', 'scoring_model'
        )


class ProblemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Problem
        fields = ('id', 'name', 'pcms_id', 'last_check_time')


class ContestProblemSerializer(serializers.ModelSerializer):
    problem = ProblemSerializer()
    contest = ContestSerializer()

    class Meta:
        model = ContestProblem
        fields = ('problem', 'contest', 'alias', 'last_check_time', 'threshold')


class AttemptSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    participant = ParticipantSerializer()
    problem_contest = ContestProblemSerializer()
    # participant_name = serializers.ReadOnlyField(source='participant.name')

    class Meta:
        model = Attempt
        fields = (
            'id', 'outcome', 'participant', 'language', 'status', 'outcome', 'time', 'score', 'alias', 'problem_contest'
        )


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'id')


class JobSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer()

    class Meta:
        model = Job
        fields = ('id', 'user')


class AttemptsCheckJobsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    attempt_lhs = AttemptSerializer()
    attempt_rhs = AttemptSerializer()
    # job = JobSerializer()

    class Meta:
        model = AttemptsCheckJobs
        fields = ('id', 'attempt_lhs', 'attempt_rhs', 'script_checking_result',
                  'status', 'checking_start_time', 'checking_end_time', 'manual_check_time')
