from dataclasses import field
from django import forms

from Order.models import Address
from .models import Account

# Create your forms here.

class RegistrtationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={
		'placeholder':'Enter Password'
	}))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={
		'placeholder':'Enter Password'
	})) 
    class Meta:
        model=Account
        fields=['first_name','last_name' ,'email','mobile' ,'password','confirm_password']
    def clean(self):
        cleaned_data    =super(RegistrtationForm,self).clean()
        password        =cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Password does not match")    

class UserUpdationForm(forms.ModelForm):
    class Meta:
        model=Account
        fields=['first_name','last_name' ,'email','mobile','profile_image']

class AddAddress(forms.ModelForm):
    class Meta:
        model = Address
        fields=['first_name','last_name','phone','email','address_line_1','address_line_2','country','state','city']



