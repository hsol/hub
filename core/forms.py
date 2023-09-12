from datetime import timedelta

from django import forms
from django.contrib.auth.models import User
from django.utils.timezone import now
from rest_framework.authtoken.models import Token


class EmailLoginForm(forms.Form):
    email = forms.CharField(
        label="이메일",
        strip=False,
        widget=forms.EmailInput(attrs={"placeholder": "example@email.com"}),
    )
    next = forms.CharField(widget=forms.HiddenInput(), required=False)

    def clean(self):
        form_data = self.cleaned_data
        if not User.objects.filter(email=form_data["email"]).exists():
            raise forms.ValidationError("해당 이메일로 계정이 존재하지 않습니다. 관리자에게 문의해주세요.")

        return form_data


class EmailTokenProcessForm(forms.Form):
    email = forms.CharField(widget=forms.HiddenInput())
    token = forms.CharField(widget=forms.HiddenInput())

    def clean(self):
        form_data = self.cleaned_data
        if not User.objects.filter(email=form_data["email"]).exists():
            raise forms.ValidationError("해당 이메일로 계정이 존재하지 않습니다. 관리자에게 문의해주세요.")

        try:
            token = Token.objects.get(key=form_data["token"])

            if token.created < now() - timedelta(minutes=5):
                raise forms.ValidationError(
                    "로그인 링크가 만료되었습니다. 로그인 링크는 받은 시점으로부터 5분간만 유효합니다. 로그인을 처음부터 다시 시도해주세요."
                )
        except Token.DoesNotExist:
            raise forms.ValidationError("토큰이 만료되었거나 존재하지 않습니다. 로그인을 처음부터 다시 시도해주세요.")
