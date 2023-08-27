from django import forms
from .models import CustomUser, Project, Subject

class RegisterForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'birth_date', 'id_number', 'role','password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'birth_date': forms.DateInput(attrs={'class':'form-control'}),
            'id_number': forms.TextInput(attrs={'class':'form-control'}),
            'role': forms.Select(attrs={'class':'form-control'}),
            'password' : forms.PasswordInput(attrs={'class':'form-control'})
        }
class LoginForm(forms.Form):
    id_number = forms.CharField(label='ID Number', max_length=30)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'subject', 'file','status', 'feedback']
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name','code']
    
