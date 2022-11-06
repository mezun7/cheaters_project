from cheaters_project.settings import main_pcms_api_url
from checker.models import Group


def get_api_url(group: Group = None):
    if group is None:
        return main_pcms_api_url
    return group.api_url
