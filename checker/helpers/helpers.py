from checker.models import Group


def get_menu_info(request):
    groups = Group.objects.filter(users_have_access__in=[request.user])
    attempts_to_check = -100
    remaining_attempts_checking_running = -1
    page_title = "test"
    all_approved_cheaters = -1
    context = {
        'groups': groups,
        'attempts_to_check': attempts_to_check,
        'remaining_attempts_checking_running': remaining_attempts_checking_running,
        'page_title': page_title.capitalize(),
        'all_approved_cheaters': all_approved_cheaters,
    }
    return context
