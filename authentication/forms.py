from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


Profile = get_user_model()


class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'E-mail'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password'
            }
        )
    )

    def clean(self):
        try:
            self.cleaned_data['email'] = self.cleaned_data['email'].strip()
        except KeyError:
            raise ValidationError('Email is not Valid!')

        return super().clean()


class ProfileRegistrationForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ("email",)
