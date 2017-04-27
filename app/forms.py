from django.contrib.auth import get_user_model
from django import forms
from django.forms import ModelForm


class LoginForm(forms.Form):
    username = forms.CharField(
        label="username",
        max_length=128,
        widget=forms.TextInput(
            attrs={
                'maxlength': 30,
                'class': 'form-control',
                'placeholder': "Username"
            }
        )
    )
    password = forms.CharField(
        label="password",
        max_length=128,
        widget=forms.PasswordInput(
            attrs={
                'maxlength': 30,
                'class': 'form-control',
                'placeholder': "Password"
            }
        )
    )


class PasswordForm(forms.Form):
    password = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(
            attrs={
                'maxlength': 30,
                'class': 'form-control',
                'placeholder': "Password"
            }
        ),
        label="Enter password"
    )
    password2 = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(
            attrs={
                'maxlength': 30,
                'class': 'form-control',
                'placeholder': "Confirm your password"
            }
        ),
        label="Enter password (again)"
    )

    def clean_password2(self):
        password = self.cleaned_data.get('password', '')
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError("Confirmation password doesn't match.")
        return password2


class SignupForm(PasswordForm):
    username = forms.CharField(
        label="username",
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                'maxlength': 30,
                'class': 'form-control',
                'placeholder': "Username"
            }
        )
    )
    first_name = forms.CharField(
        label="first name",
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                'maxlength': 30,
                'class': 'form-control',
                'placeholder': "First Name"
            }
        )

    )
    last_name = forms.CharField(
        label="last name",
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                'maxlength': 30,
                'class': 'form-control',
                'placeholder': "Last Name"
            }
        )
    )
    email = forms.EmailField(
        label="email",
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={
                'maxlength': 60,
                'class': 'form-control',
                'placeholder': "Email Address"
            }
        )
    )

    field_order = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']


class UserProfileForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']


class AddFriendForm(forms.Form):
    username = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
