from django import forms
from .models import Commande
from .models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['adresse', 'telephone', 'email', 'livraison', 'mode_paiement']
        widgets = {
            'mode_paiement': forms.RadioSelect(),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'telephone', 'photo_profil', 'langue', 'newsletter']

class PasswordChangeCustomForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'telephone', 'password1', 'password2']

class ConnexionForm(AuthenticationForm):
    pass
