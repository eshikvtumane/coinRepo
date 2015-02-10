#-*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from users.models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

# Override UserCreationForm
# http://www.djangobook.com/en/2.0/chapter14.html
# http://stofl.org/questions/5745197/django-create-custom-usercreationform-basic
class RegisterForm(UserCreationForm):
    username = forms.RegexField(label=_(u'Логин'), max_length=30, regex=r'^[\w.@+-]+$',
        help_text = _(u"Вводите только буквы и числа, не более 30-ти символов."),
        error_messages = {'invalid': _(u"Вводите только буквы и числа."),
                          'required': _(u'Обязательное поле')})
    email = forms.EmailField(label='Email', required=True,
        error_messages = {'invalid': _(u'Введите правильный email'),
                          'required': _(u'Обязательное поле')})
    password1 = forms.CharField(label=_(u'Пароль'),
        widget=forms.PasswordInput,
        error_messages={'required': _(u'Обязательное поле')})
    password2 = forms.CharField(label=_(u'Повторите пароль'),
        widget=forms.PasswordInput,
        help_text=_(u"Введите тот же пароль, что и выше, для проверки."),
        error_messages={'required': _(u'Обязательное поле')})

    error_messages = {
        'duplicate_username': _(u"Пользователь с таким логином уже существует"),
        'password_mismatch': _(u"Пароли не совпадают."),
        'required': _(u'Обязательное поле')
    }

    # Check email for unique
    # http://stackoverflow.com/questions/5773970/django-auth-user_image-with-unique-email
    def clean_email(self):
        data = self.cleaned_data['email']

        if User.objects.filter(email=data).exists():
            raise forms.ValidationError(u'Email уже используется')
        return data

    class Meta:
        model = User
        fields = ['username', 'email']

class AuthForm(forms.Form):
    username = forms.RegexField(label=_(u'Логин'), required=True, max_length=30, regex=r'^[\w.@+-]+$',
                                error_messages = {'invalid': _(u"Вводите только буквы и числа."),
                                                  'required': _(u'Обязательное поле')})
    password = forms.CharField(label=_(u'Пароль'),
                                widget=forms.PasswordInput,
                                error_messages={'required': _(u'Обязательное поле')})

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'middle_name', 'avatar']

class CustomUserForm(forms.Form):
    email = forms.EmailField(label='Email', required=False,
        error_messages = {'invalid': _(u'Введите правильный email'),
                          'required': _(u'Обязательное поле')})

    def clean_email(self):
        data = self.cleaned_data['email']

        if User.objects.filter(email=data).exists():
            raise forms.ValidationError(u'Email уже используется')
        return data
