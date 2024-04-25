from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django import forms

from content.forms import StyleFormMixin
from users.models import User, PaymentSubscription


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ['phone_number', 'password1', 'password2']


class UserUpdateForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ['phone_number', 'full_name', 'avatar', 'email',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class PaymentSubscriptionForm(forms.ModelForm):
    class Meta:
        model = PaymentSubscription
        fields = ['subscription_period']


class CancelSubscriptionForm(StyleFormMixin, forms.Form):
    confirm_cancel = forms.BooleanField(label='I confirm cancellation', required=True)


class CustomAuthenticationForm(AuthenticationForm):
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None or not self.user_cache.is_active:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
        return cleaned_data
