from django import forms
from dashboard.models import Course
from django.contrib.auth.models import User

class AddCourseForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'name'}))
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'description'}))
    participants = forms.ModelMultipleChoiceField(required=True, queryset=User.objects.filter(groups__name__in=('student','teacher')).all(), widget=forms.SelectMultiple(attrs={'class': 'form-select', 'placeholder': 'participants'}))

    class Meta:
        model = Course
        fields = ('name', 'description', 'participants')

class EditCourseForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'name'}))
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'description'}))
    participants = forms.ModelMultipleChoiceField(required=True, queryset=User.objects.filter(groups__name__in=('student','teacher')).all(), widget=forms.SelectMultiple(attrs={'class': 'form-select', 'placeholder': 'participants'}))

    class Meta:
        model = Course
        fields = ('name', 'description', 'participants')