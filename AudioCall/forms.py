from django import forms
from AudioCall.models import Contact


class ContactForm(forms.ModelForm):
    """
    Simple contact form if cutomer want to contact
    """

    class Meta:
        model = Contact
        fields = [
            'name',
            'email',
            'subject',
            'comment',
        ]
