from django.contrib.auth.forms import UserCreationForm, UserChangeForm
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
