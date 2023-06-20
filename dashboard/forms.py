from django import forms
from dashboard.models import Course

class AddCourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ('title', 'description', 'participants')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form_input'}),
            'description': forms.TextInput(attrs={'class': 'form_input'}),
            'participants': forms.MultipleHiddenInput(attrs={'class': 'form_input'}),
        }