from django import forms
from .models import tweet

class tweetform(forms.ModelForm):
    class meta:
        model=tweet
        fields=['text','photo']