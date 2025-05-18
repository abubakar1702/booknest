from django import forms
from .models import UsersList, UsersBook



class ListCreationForm(forms.Form):
    name = forms.CharField(max_length=200)
    books = forms.ModelMultipleChoiceField(
        queryset=UsersBook.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label = "Select books to add"
        )
    