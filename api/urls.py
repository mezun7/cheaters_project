from django.template.defaulttags import url
from django.urls import path, include
from rest_framework import routers

from api import views

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'participants', views.ParticipantViewSet)
router.register(r'contests', views.ContestViewSet)
router.register(r'attempts', views.AttemptViewSet)
router.register(r'acj', views.AttemptsCheckJobsViewSet, basename='AttemptsCheckJobs')
router.register(r'checkings_in_progress', views.CheckingInProgressViewSet, basename='AttemptsCheckJobsInProgress')
router.register(r'pending_manual_check', views.PendingManualCheckViewSet, basename='PendingManualCheck')
router.register(r'list_of_cheaters', views.ListOfCheatersViewSet, basename='ListOfCheaters')

urlpatterns = [
    path('api/', include(router.urls)),
    path('test/', views.test)
    # path('remove_groupoup/<int:group_id>/', views.test, name='test'),
]
