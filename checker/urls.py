import datetime

from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views

from checker import views
from checker.forms import LoginForm

app_name = 'mainapplication'

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
    path('contest/<int:contest_id>/', views.contest, name='contest'),
    path('pending_manual_check/', views.pending_manual_check, name='pending_manual_check'),
    path('automatic_checking/', views.automatic_checking, name='automatic_checking'),
    path('all_cheaters/', views.all_cheaters, name='all_cheaters')
    # path('contests/<int:group_id>', views.list_of_contests, name='list_of_contests'),
    # path('contest/<int:contest_pk>', views.contest_result, name='contest_result')
    # path('test/', views.test_upload, name='test-upload'),
]
