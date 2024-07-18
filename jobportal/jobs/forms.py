from django import forms
from .models import Job

from .models import JobApplication

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company_name', 'description', 'location', 'salary', 'requirements','company_logo']


# forms.py



class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['name','email', 'phone_number', 'resume', 'year_of_passout', 'qualification']
        labels = {
            'name':'Name',
            'phone_number': 'Phone Number',
            'year_of_passout': 'Year of Passout',
            'qualification': 'Qualification',
        }
        widgets = {
            'resume': forms.FileInput(attrs={'accept': '.pdf,.doc,.docx'}),
        }


class UpdateStatusForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['status']