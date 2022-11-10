from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from checker.models import Job


# Create your views here.
@login_required()
def main(request):
    return HttpResponse(f"Hello {request.user}")


def login_auth(request):
    pass
