from django import forms
from django.contrib.auth import authenticate, login


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', required=True, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label='Password', required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cd          = self.cleaned_data
        logged_in   = False
        user        = authenticate(username=cd['username'], password=cd['password'])

        if user is not None:
            if user.is_active:
                login(self.request, user)
                logged_in = True

        if not logged_in:
            self.add_error(None, 'Authorization unsuccessful')


class SearchForm(forms.Form):
    search = forms.CharField(label='Search',required=False)