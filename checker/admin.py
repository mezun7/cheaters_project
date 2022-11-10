from django.contrib import admin

# Register your models here.

from django.contrib import admin

# Register your models here.
from django.contrib.admin import TabularInline

from checker.models import Group, Contest, Problem, Attempt, Participant, ContestProblem, FileUploadTest, UserType


# @admin.register(Group)
# class AdminGroup(admin.ModelAdmin):
#     list_display = ('name', 'login', 'pcms_url')


class ContestProblemInlineAdmin(TabularInline):
    model = Contest.problem.through
    extra = 0


@admin.register(Contest)
class AdminContest(admin.ModelAdmin):
    # fields = ['problem']
    list_display = ('name', 'group', 'pcms_id', 'contest_id')
    list_filter = ('group',)
    inlines = [
        ContestProblemInlineAdmin,
    ]


@admin.register(Problem)
class AdminProblem(admin.ModelAdmin):
    list_display = ('name', 'pcms_id', 'last_check_time')


@admin.register(Attempt)
class AdminAttempt(admin.ModelAdmin):
    list_display = ('participant', 'problem_contest', 'outcome', 'score', 'time')


@admin.register(Participant)
class AdminParticipant(admin.ModelAdmin):
    list_display = ('name', 'pcms_id')


@admin.register(ContestProblem)
class AdminContestProblem(admin.ModelAdmin):
    list_display = ('problem', 'contest', 'alias')


@admin.register(UserType)
class AdminUserType(admin.ModelAdmin):
    list_display = ('user', 'auth_type', 'login_pcms', 'password_pcms')


@admin.register(FileUploadTest)
class AdminFileUploadTest(admin.ModelAdmin):
    list_display = ('file',)
