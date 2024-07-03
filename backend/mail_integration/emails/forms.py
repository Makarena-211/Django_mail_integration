from django import forms
from .models import EmailAccount, EmailMessage

class LoginForm(forms.ModelForm):
    class Meta:
        model = EmailAccount
        fields = ['email', 'password']
        

class MessageForm(forms.ModelForm):
    class Meta:
        model = EmailMessage
        fields = ['email', 'topic', 'date_sent', 'date_recieved', 'body', 'attachments']
