from django import forms
from .models import Vtuber, Group, Song


class VtuberForm(forms.ModelForm):
    class Meta:
        model = Vtuber
        fields = [field.name for field in Vtuber._meta.fields]
