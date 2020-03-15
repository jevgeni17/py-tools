from django import forms
from django.forms import TextInput
 
class UserForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'BOOK TITLE'}))