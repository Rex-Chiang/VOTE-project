from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label = "name", max_length = 10)
    password = forms.CharField(label = "password", widget = forms.PasswordInput())
        