from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from cheaters_project import settings
from checker.entities.entities import CODEMIRROR_LANG_PARAMS
from checker.forms import ContestProblemEditForm
from checker.helpers.helpers import get_menu_info, get_raw_str
from checker.models import Group, Contest, ContestProblem, AttemptsCheckJobs
import os

@login_required()
def edit_contest_threshold(request, group_id, contest_id):
    group = Group.objects.get(pk=group_id)
    contest = Contest.objects.get(pk=contest_id)
    contest_problems = contest.contestproblem_set.all().order_by('alias')
    ContestProblemsFormSet = modelformset_factory(ContestProblem, form=ContestProblemEditForm,
                                                  max_num=len(contest_problems))
    formset = ContestProblemsFormSet(queryset=contest_problems)
    context = get_menu_info(request, f"{group.name}: {contest.name}")
    context['contest_problems'] = contest_problems
    context['formset'] = formset
    context['group'] = group
    context['contest'] = contest
    if request.POST:
        formset2 = ContestProblemsFormSet(request.POST)
        if formset2.is_valid():
            formset2.save()
        return HttpResponseRedirect(reverse('checker:edit_contest_threshold',
                                            kwargs={'group_id': group_id, "contest_id": contest_id}))
    return render(request, 'checker/contest_problem.html', context=context)



