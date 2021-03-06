from django import forms
from django.contrib.auth.models import User
from django.core import validators
from django.forms import ModelForm
 
def isValidUsername(field_data):
    try:
        User.objects.get(username=field_data)
    except User.DoesNotExist:
        return
    raise validators.ValidationError('The username "%s" is already taken.' % field_data)

def uniqueEmail(field_data):
    try:
        User.objects.get(email=field_data)
    except User.DoesNotExist:
        return
    raise validators.ValidationError('The email address "%s" is already in use.' % field_data) 

class RegistrationForm(forms.Form):
    
    username = forms.CharField(min_length=1, max_length=30, validators=[validators.RegexValidator(
                regex="^[a-zA-Z0-9]*$", message=u"Only letters and numerals are allowed.", code="custom"), isValidUsername])
    email = forms.EmailField() # XXX_DWIGHT removing unique email for now - logic
    # is that user can have multiple accounts with delta companies
    password1 = forms.CharField(label="Password", min_length=1, max_length=30, widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", min_length=1, max_length=30, widget=forms.PasswordInput)
    
    def clean(self):
        #There are already errors, don't raise more
        if 'password1' not in self.cleaned_data or 'password2' not in self.cleaned_data:
            return self.cleaned_data
        if self.cleaned_data['password1'] == self.cleaned_data['password2']:
            return self.cleaned_data
        else:
            raise validators.ValidationError("passwords must match")
    
    def passwordsMatch(self):
        return self.password1 != self.password2
    
    def save(self):
        u = User.objects.create_user(username=self.cleaned_data['username'],
                                     email=self.cleaned_data['email'],
                                     password=self.cleaned_data['password1'])
        return u


class LoginForm(forms.Form):
    username = forms.CharField(min_length=1, max_length=30, validators=[validators.RegexValidator(
                regex="^[a-zA-Z0-9]*$", message=u"Only letters and numerals are allowed.", code="custom"), isValidUsername])
    password = forms.CharField(label="Password", min_length=1, max_length=30, widget=forms.PasswordInput)

