from django import forms
from django.contrib.auth.models import User
from .models import Project,Attachment
from teams.models import Team
from tempus_dominus.widgets import DatePicker 
from .utils import STATUS_CHOICES,STATUS_PRIORITY

class ProjectForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows':3,'placeholder':"Enter Project Description"})
        , label=False
        , required=True
        )
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder':"Enter Project Name"})
        , label=False
        , required=True
        )
    team = forms.ModelChoiceField(
        queryset=Team.objects.all(), 
        widget=forms.Select(
            attrs={"class":"form-control"}
        ),
        label=False, 
        required=False
        )
    status=forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(
            attrs={"class":"form-control"}
        ),
        label=False,
        required=True
    )
    priority=forms.ChoiceField(
        choices=STATUS_PRIORITY,
        widget=forms.Select(
            attrs={"class":"form-control"}
        ),
        label=False,
        required=True
    )
    client_company = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder':"Enter Client Company"})
        , label=False
        , required=True
        )
    
    
    start_date = forms.DateField(
        widget=DatePicker(
            attrs={
                "append":"fa fa-calendar",
                "icon_toggle":True
            }
        ),
        label=False,
        required=True
    )
    due_date = forms.DateField(
        widget=DatePicker(
            attrs={
                "append":"fa fa-calendar",
                "icon_toggle":True
            }
        ),
        label=False,
        required=True
    )
    total_amount=forms.DecimalField(
        label=False,
        required=False
    )
    amount_spent=forms.DecimalField(
        label=False,
        required=False
    )
    estimated_duration=forms.DecimalField(
        label=False,
        required=False
    )
    class Meta:
        model = Project
        fields = ['name',  'team','description', 'status', 'priority','client_company', 'start_date', 'due_date'
                  ,'total_amount','amount_spent','estimated_duration']
        

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file']