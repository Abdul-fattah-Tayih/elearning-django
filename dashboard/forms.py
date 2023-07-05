from django import forms
from dashboard.models import Course, Lesson, LessonCompletion, User
from dashboard.validators import InList

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

class LessonForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'name'}))
    content = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'description'}))

    class Meta:
        model = Lesson
        fields = ('name', 'content')

class LessonCompletionForm(forms.Form):
    completion = forms.CharField(required=True, widget=forms.HiddenInput(), validators=[InList([LessonCompletion.ACTION_COMPLETE, LessonCompletion.ACTION_INCOMPLETE])])

class LessonCommentForm(forms.Form):
    content = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your comment'}))