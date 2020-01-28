from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'v-model': 'login_form["username"]',
            }
        )
    )
    password = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password',
                'v-model': 'login_form["password"]',
            }
        )
    )

class SignupForm(forms.Form):
    username = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username',
                'v-model': 'signup_form["username"]',
            }
        )
    )
    email = forms.EmailField(
        max_length=200,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'E-mail',
                'v-model': 'signup_form["email"]',
            }
        )
    )
    password = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password',
                'v-model': 'signup_form["password"]',
            }
        )
    )