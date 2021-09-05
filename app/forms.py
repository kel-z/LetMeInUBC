from django import forms


class CourseForm(forms.Form):
    session = forms.ChoiceField(choices=[('W', 'Winter'), ('S', 'Summer')], required=True, widget=forms.Select(attrs={'class':'djform', 'id':'sess'}))
    year = forms.CharField(min_length=4, max_length=4, required=True, widget=forms.TextInput(attrs={'class':'djform', 'id':'year'}))
    dept = forms.CharField(min_length=4, max_length=4, required=True, widget=forms.TextInput(attrs={'class':'djform', 'id':'dept'}))
    course = forms.CharField(min_length=3, max_length=4, required=True, widget=forms.TextInput(attrs={'class':'djform', 'id':'cnum'}))
    section = forms.CharField(min_length=3, max_length=3, required=True, widget=forms.TextInput(attrs={'class':'djform', 'id':'sect'}))
    only_general = forms.BooleanField(initial=True, label="Only General Seats?", required=False, widget=forms.CheckboxInput(attrs={'class':'djform', 'id':'onge'}))
    sms = forms.CharField(min_length=10, max_length=10, required=False, widget=forms.TextInput(attrs={'class':'djform', 'id':'sms'}))
    email = forms.EmailField(max_length=30, required=False, widget=forms.TextInput(attrs={'class':'djform', 'id':'email'}))