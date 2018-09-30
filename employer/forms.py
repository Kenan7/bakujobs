from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from .models import Employer
from django import forms


User = get_user_model()


class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('name', 'email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('name', 'email', 'password', 'active', 'admin')

    def clean_password(self):
        return self.initial["password"]


class LoginForm(forms.Form):
    email    = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'input100'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'input100'
        })


class RegisterForm(forms.ModelForm):
    password1   = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2   = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    location    = forms.CharField(label='Company Location')
    website     = forms.CharField(label='Company Website')
    phone       = forms.IntegerField(label='Company phone number')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'input100'
            })
        self.fields['name'].widget.attrs.update({
            'placeholder': 'Company name'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Company e-mail'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'New password'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Retype password'
        })
        self.fields['website'].widget.attrs.update({
            'placeholder': 'Company website'
        })
        self.fields['location'].widget.attrs.update({
            'placeholder': 'Company location'
        })
        self.fields['phone'].widget.attrs.update({
            'placeholder': 'Company phone number'
        })

    class Meta:
        model = Employer
        fields = ('name', 'email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user