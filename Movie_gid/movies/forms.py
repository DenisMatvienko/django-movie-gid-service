from django import forms
from snowpenguin.django.recaptcha3.fields import ReCaptchaField

from .models import Reviews, Rating, RatingStars


class ReviewForm(forms.ModelForm):
    """ Review form with fields for add review """
    captcha = ReCaptchaField()

    class Meta:
        model = Reviews
        fields = ('name', 'email', 'text', 'captcha')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control border'}),
            'email': forms.EmailInput(attrs={'class': 'form-control border'}),
            'text': forms.Textarea(attrs={'class': 'form-control border'})
        }


#   Форма добавления рейтинга
class RatingForm(forms.ModelForm):
    """ Rating form with stars field for making rating """
    star = forms.ModelChoiceField(queryset=RatingStars.objects.all(), widget=forms.RadioSelect(), empty_label=None)

    class Meta:
        model = Rating
        fields = ('star',)