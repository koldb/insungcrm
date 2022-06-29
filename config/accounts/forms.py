from django import forms
from django.contrib.auth.models import User
from .models import User
from argon2 import PasswordHasher, exceptions
from django.shortcuts import render, redirect

#회원가입 폼
class RegisterForm(forms.ModelForm):
    user_id = forms.CharField(
        label='아이디',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'user_id',
                'id': 'user_id',
                'placeholder': '아이디'
            }
        ),
        error_messages={'required': '아이디를 입력하세요.', 'unique': '중복된 아이디 입니다.'}
    )
    user_name = forms.CharField(
        label='성함',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'user_name',
                'id': 'user_name',
                'placeholder': '성함'
            }
        ),
        error_messages={'required': '성함을 입력하세요.'}
    )
    user_pw = forms.CharField(
        label='비밀번호',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'user_pw',
                'id': 'user_pw',
                'placeholder': '비밀번호'
            }
        ),
        error_messages={'required': '비밀번호를 입력하세요.'}
    )
    user_pw2 = forms.CharField(
        label='비밀번호 확인',
        required='True',
        widget=forms.PasswordInput(
            attrs={
                'class': 'user_pw2',
                'id': 'user_pw2',
                'placeholder': '비밀번호 확인'
            }
        ),
        error_messages={'required': '비밀번호가 일치하지 않습니다.'}
    )
    cname = forms.CharField(
        label='업체명',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'cname',
                'id': 'cname',
                'placeholder': '업체명'
            }
        ),
        error_messages={'required': '업체명을 입력하세요.'}
    )
    user_phone = forms.CharField(
        label='연락처',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'user_phone',
                'id': 'user_phone',
                'placeholder': '000-0000-0000'
            }
        ),
        error_messages={'required': '연락처를 입력하세요.'}
    )
    user_email = forms.EmailField(
        label='이메일',
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'user_email',
                'id': 'user_email',
                'placeholder': '이메일'
            }
        ),
        error_messages={'required': '이메일을 입력하세요.'}
    )
    user_dept = forms.CharField(
        label='부서명',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'user_dept',
                'id': 'user_dept',
                'placeholder': '부서명'
            }
        ),
        error_messages={'required': '부서명을 입력하세요.'}
    )
    field_order = [
        'user_id',
        'cname',
        'user_name',
        'user_pw',
        'user_pw2',
        'user_phone',
        'user_email',
        'user_dept'
    ]

    class Meta:
        model = User
        fields = [
            'user_id',
            'cname',
            'user_name',
            'user_pw',
            'user_phone',
            'user_email',
            'user_dept'
        ]

    def clean(self):
        cleaned_data = super().clean()

        user_id = cleaned_data.get('user_id', '')
        cname = cleaned_data.get('cname', '')
        user_name = cleaned_data.get('user_name', '')
        user_pw = cleaned_data.get('user_pw', '')
        user_pw2 = cleaned_data.get('user_pw2', '')
        user_phone = cleaned_data.get('user_phone', '')
        user_email = cleaned_data.get('user_email', '')
        user_dept = cleaned_data.get('user_dept', '')

        if user_pw != user_pw2:
            print("비번 틀림")
            return self.add_error('user_pw2', '비밀번호가 다릅니다.')
        elif 4 > len(user_id) or len(user_id) > 16:
            return self.add_error('user_id', '아이디는 4~16글자로 입력하세요.')
        elif 4 > len(user_pw):
            return self.add_error('user_pw', '비밀번호는 4자 이상으로 적어주세요')
        else:
            self.user_id = user_id
            self.cname = cname
            self.user_name = user_name
            self.user_pw = PasswordHasher().hash(user_pw)
            self.user_pw2 = user_pw2
            self.user_phone = user_phone
            self.user_email = user_email
            self.user_dept = user_dept


class LoginForm(forms.Form):
    user_id = forms.CharField(
        max_length=32,
        label='아이디',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'user_id',
                'placeholder': '아이디'
            }
        ),
        error_messages={'required': '아이디를 입력하세요.'}
    )
    user_pw = forms.CharField(
        max_length=128,
        label='비밀빈호',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'user_pw',
                'placeholder': '비밀번호'
            }
        ),
        error_messages={'required': '비밀번호를 입력하세요.'}
    )

    field_order = [
        'user_id',
        'user_pw',
    ]

    def clean(self):
        cleaned_data = super().clean()

        user_id = cleaned_data.get('user_id', '')
        user_pw = cleaned_data.get('user_pw', '')

        if user_id == '':
            return self.add_error('user_id', '아이디를 다시 입력 하세요.')
        elif user_pw == '':
            return self.add_error('user_id', '비밀번호를 다시 입력 하세요.')
        else:
            try:
                user = User.objects.get(user_id=user_id)
            except User.DoesNotExist:
                return self.add_error('user_id', '아이디가 다릅니다.')

            try:
                PasswordHasher().verify(user.user_pw, user_pw)
            except exceptions.VerifyMismatchError:
                return self.add_error('user_pw', '비밀번호가 다릅니다.')
            self.login_session = user.cname
            self.user_dept = user.user_dept
            self.user_name = user.user_name
            self.user_phone = user.user_phone

