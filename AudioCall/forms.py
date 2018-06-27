from django import forms
from .models import *


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = [
            'name',
            'email',
            'subject',
            'comment',
        ]
