from django import forms
from .models import Contact
from snowpenguin.django.recaptcha3.fields import ReCaptchaField


#   Форма подписки по email
class ContactForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Contact
        fields = ('email', 'captcha')
        widgets = {
            'email': forms.TextInput(attrs={'class': 'editContent', 'placeholder': 'Ваш email...'})
        }
        labels = {
            'email': ''
        }