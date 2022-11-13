from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from cheaters_project.settings import main_pcms_api_url
from checker.helpers.helpers import check_login_password_exists
from checker.models import Group, ContestProblem


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': 'Логин'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль', 'class': 'form-control '
                                                                                                   'form-control-user'}))


class GroupAddForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = ['users_have_access']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-control-user',
                'placeholder': 'Название группы'
            }),
            'login': forms.TextInput(attrs={
                'class': 'form-control form-control-user',
                'placeholder': 'Логин от pcms'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control form-control-user',
                'placeholder': 'Пароль от pcms'
            }),
            'api_url': forms.TextInput(attrs={
                'class': 'form-control form-control-user',
                'placeholder': 'Необязательно: адрес pcms api, default: pcms.litsey2.ru',
            }),
        }

    def clean(self):
        login = self.cleaned_data.get('login', '')
        password = self.cleaned_data.get('password', '')
        api_url = self.cleaned_data.get('api_url', '')
        api_url = api_url if api_url else main_pcms_api_url
        continue_check = True if login and password else False
        # print(login, password, api_url)
        if check_login_password_exists(login, password, api_url) and continue_check:
            return self.cleaned_data
        raise ValidationError(f'Login password in pcms server doesn\'t exists [{login, password}]')


class ContestProblemEditForm(forms.ModelForm):
    class Meta:
        model = ContestProblem
        exclude = ['problem', 'contest', 'last_check_time', 'alias']

        widgets = {
            'threshold': forms.NumberInput(attrs={
                'class': 'form-control form-control-user',
                'placeholder': 'Погрешность'
            })
        }

    def clean_threshold(self):
        try:
            threshold = self.cleaned_data.get('threshold', '')
            print(threshold)
            threshold = float(threshold)
            if (not 0.0 <= threshold <= 1.0) or threshold == -1.0:
                raise ValidationError(f'Threshold should be between 0.0 and 1.0 or -1.0. You entered {threshold}')
            return threshold
        except UnboundLocalError:
            return threshold
        except TypeError:
            return threshold
