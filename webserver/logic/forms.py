from django import forms
from django.contrib.auth import authenticate

from voteapp.models import Vote, User, VoteType
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.password_validation import NumericPasswordValidator, \
    UserAttributeSimilarityValidator, CommonPasswordValidator,\
    MinimumLengthValidator
from django.forms.widgets import HiddenInput

class VoteForm(forms.Form):
    choice = forms.IntegerField(widget = HiddenInput(), min_value=1, max_value=3)
    
    def clean(self):
        valid = [1, 2, 3]
        if self.cleaned_data.get('choice') not in valid:
            raise forms.ValidationError('Vote not valid')


class SignupForm(forms.Form):
    username = forms.CharField(min_length=4, max_length=150,
                               validators=[UnicodeUsernameValidator()])
    validators = [MinimumLengthValidator(min_length=6).validate,
                  CommonPasswordValidator().validate,
                  UserAttributeSimilarityValidator().validate,
                  NumericPasswordValidator().validate]
    password = forms.CharField(widget=forms.PasswordInput,
                               validators=validators)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['password2'].label = "Password repeat"

    def clean_username(self):
        """
            Asegura que el usuario no existe
            @author Joaquin
        """
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'A user with that username already exists')
        return username

    def clean(self):
        """
            Las contraseñas coinciden
            @author Joaquin
        """
        password_1 = self.cleaned_data.get('password')
        password_2 = self.cleaned_data.get('password2')
        if password_1 != password_2:
            raise forms.ValidationError(
                'Password and Repeat password are not the same')


class SigninForm(forms.Form):
    """
        Formulario de inicio de sesión
    """
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        """
            El usuario se encuentra en la base de datos
            @author Joaquin
        """
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if authenticate(username=username, password=password) is None:
            raise forms.ValidationError('Username/password is not valid')
