from django import forms

class enrollForm(forms.Form):
    course_id = forms.CharField(label='course_id', max_length=10)