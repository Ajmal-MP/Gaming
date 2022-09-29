from django import forms
from Accounts.models import Account


class UserForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ['is_active'] 

    def __str__(self):
        return self.first_name