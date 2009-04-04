from django import forms

from models import Account

class AccountForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput, help_text="Will be sent over the wire unencrypted!")
    class Meta:
        model = Account