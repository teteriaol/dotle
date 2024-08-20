from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class HeroForm(forms.Form):
    hero_field = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'input__field', 'placeholder':'Type the name of any hero...'}))


class LoginForm(forms.Form):
    logusername = forms.CharField(max_length=25, widget=forms.TextInput(attrs={'class': 'login-input'}))
    logpassword = forms.CharField(max_length=25, widget=forms.PasswordInput(attrs={'class':'password-login login-input'}))
    

class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length=20)
    email = forms.CharField(max_length=20)
    password1 = forms.CharField(label='Password', strip=False, max_length=20, widget=forms.PasswordInput(attrs={'class':'password-field'}))
    password2 = forms.CharField(max_length=20, strip=False,  widget=forms.PasswordInput(attrs={'class':'password-field'}))
    
	
    def clean_password(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 4:
            raise forms.ValidationError('Password too short')
        return super(RegisterForm, self).clean_password1()
	
    class Meta:
        model=User
        fields = ['username','email','password1','password2'] 


class ChangeForm(forms.Form):
    changeusername = forms.CharField(max_length=20, required=False)
    changeemail = forms.CharField(max_length=20, required=False) 
    changenewpassword = forms.CharField(strip=False, max_length=20, widget=forms.PasswordInput(attrs={'class':'password-field'}), required=False)
    changepassword1 = forms.CharField(strip=False, max_length=20, widget=forms.PasswordInput(attrs={'class':'password-field'}))
    changepassword2 = forms.CharField(max_length=20, strip=False,  widget=forms.PasswordInput(attrs={'class':'password-field'}))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ChangeForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['changeusername'].initial = user.username
            self.fields['changeemail'].initial = user.email

class DeleteAllForm(forms.Form):
    deleteall = forms.CharField(max_length=27, required=True, widget=forms.TextInput(attrs={'autocomplete':'off'}))
        