from django import forms

from .models import Reviews


#   Форма отзывов
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = ('name', 'email', 'text')