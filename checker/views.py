from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User

from checker.helpers.helpers import get_menu_info
from checker.models import Job


# Create your views here.
@login_required()
def main(request):
    context = get_menu_info(request)

    return render(request, 'checker/index.html', context=context)


def login_auth(request):
    pass


@login_required()
def group(request, group_id: int):
    context = get_menu_info(request)
    return render(request, 'checker/index.html', context=context)


@login_required()
def add_group(request):
    context = get_menu_info(request)
    return render(request, 'checker/index.html', context=context)


@login_required()
def edit_group(request, group_id: int):
    context = get_menu_info(request)
    return render(request, 'checker/index.html', context=context)


@login_required()
def contest(request, contest_id: int):
    context = get_menu_info(request)
    return render(request, 'checker/index.html', context=context)


@login_required()
def pending_manual_check(request):
    context = get_menu_info(request)
    return render(request, 'checker/index.html', context=context)


@login_required()
def automatic_checking(request):
    context = get_menu_info(request)
    return render(request, 'checker/index.html', context=context)

@login_required()
def all_cheaters(request):
    context = get_menu_info(request)
    return render(request, 'checker/index.html', context=context)