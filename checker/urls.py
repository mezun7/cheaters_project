import datetime

from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views

from checker import views, contest_views, checking_views
from checker.forms import LoginForm

app_name = 'checker'

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.main, name='main_page'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('login/',
         auth_views.LoginView.as_view(
             template_name='auth/login.html',
             authentication_form=LoginForm,
             extra_context={
                 'stop_register': datetime.date.today(),
                 'year': datetime.date.today().year
             }
         ),
         name='login'
         ),
    path('group/<int:group_id>/', views.group, name='group'),
    path('group_edit/<int:group_id>/', views.edit_group, name='edit_group'),
    path('add_group/', views.add_group, name='add_group'),
    path('remove_group/<int:group_id>/', views.remove_group, name='remove_group'),
    path('contest/<int:contest_id>/', views.contest, name='contest'),
    path('pending_manual_check/', views.pending_manual_check, name='pending_manual_check'),
    path('automatic_checking/', views.automatic_checking, name='automatic_checking'),
    path('all_cheaters/', views.all_cheaters, name='all_cheaters'),
    path('my_groups/', views.my_groups, name='my_groups'),
    path('start_sync/<int:group_id>/', views.start_sync, name='start_sync'),
    path('sync_contest/<int:group_id>/<int:contest_id>/', views.sync_contest, name='sync_contest'),
    path('edit_contest_threshold/<int:group_id>/<int:contest_id>/', contest_views.edit_contest_threshold, name='edit_contest_threshold'),
    path('check_attempts/<int:attempts_check_jobs_id>/', checking_views.check_attempts, name='check_attempts'),
    path('check_my_groups/', checking_views.check_my_groups, name='check_my_groups'),
    path('check_group/<int:group_id>/', checking_views.check_group, name='check_group'),
    path('check_contest/<int:contest_id>/', checking_views.check_contest, name='check_contest'),
    path('checking_in_progress/', checking_views.checking_in_progress, name='checking_in_progress')
    # path('contests/<int:group_id>', views.list_of_contests, name='list_of_contests'),
    # path('contest/<int:contest_pk>', views.contest_result, name='contest_result')
    # path('test/', views.test_upload, name='test-upload'),
]
