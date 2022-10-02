from django import forms
from main_app.models import Film
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    password = forms.CharField(label=('Password'), widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))



class UserCreateForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    password = forms.CharField(label=('Password'), widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))
    password1 = forms.CharField(label=('Password confirmation'), widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }),
                                help_text=('Enter the same password as above, for verification.'))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise ValidationError('User already exists')
        return username

    def clean_password2(self):
        password = self.cleaned_data.get("password1")
        password1 = self.cleaned_data.get("password2")
        if password and password1 and password != password1:
            raise forms.ValidationError('password_mismatch', code='password_mismatch')
        return password1

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email):
            raise ValidationError("User's mail is already exist")
        return email


class FilmCreateForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = 'title category producer'.split()
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'producer': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }
