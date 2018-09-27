from django.contrib.auth import (
    authenticate,
    login,
    logout
)
from .models import Employer
from django import forms


class UserLoginForm(forms.Form):
    name            = forms.CharField()
    password        = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'input100'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'input100'
        })

    def clean(self, *args, **kwargs):
        name = self.cleaned_data.get("name")
        password = self.cleaned_data.get("password")

        if name and password:
            user = authenticate(name=name, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist")
                print("This user does not exist")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect passsword")
                print("Incorrect passsword")
            if not user.is_active:
                raise forms.ValidationError("This user is not longer active.")
                print("This user is not longer active.")
            print("whatever")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    email       = forms.EmailField(label='Email address')
    email2      = forms.EmailField(label='Confirm Email')
    password    = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Employer
        fields = [
            'name',
            'email',
            'email2',
            'location',
            'website',
            'phone'
        ]

    def clean_email2(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email != email2:
            raise forms.ValidationError("Emails must match")

        #
        # Gonna write AJAX request in here somewhere for checking existing email real-time
        #
        email_qs = Employer.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This email has already been registered")
        return email
