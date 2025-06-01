from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from tempus_dominus.widgets import DatePicker 
import os

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #Removing helper text
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

        # Customizing label
        self.fields['email'].label = "Email"
        self.fields['password2'].label = "Confirm password"

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control mb-2'})
            self.fields[field_name].label = field_name.replace('_', ' ').title()
            # if field_name == 'email':
            #      self.fields[field_name].label = "Email Address"
            # else:
            #     self.fields[field_name].label = field_name.replace('_', ' ').title()

        self.fields['username'].help_text = None


class ProfileUpdateForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=DatePicker(
            attrs={
                "append":"fa fa-calendar",
                "icon_toggle":True
            }
        ),
        label=False,
        required=False
    )
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control-file'})
    )
    class Meta:
        model = Profile
        fields = ['job_title', 'profile_picture', 'bio', 'location', 'phone', 'date_of_birth']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            # 'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            # 'profile_picture': forms.ClearableFileInput(),
            
        }

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('user', None)  # Pop 'user' before calling super
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name != 'date_of_birth':
                field.widget.attrs.update({'class': 'form-control mb-2'})
            field.label = field_name.replace('_', ' ').title()
            # if field_name == 'job_title':
            #     self.fields[field_name].label = "Job Title"
            # elif field_name == 'profile_picture':
            #     self.fields[field_name].label = "Profile Picture"
            # elif field_name == 'date_of_birth':
            #     self.fields[field_name].label = "Date of Birth"
            # else:
            #     self.fields[field_name].label = field_name.replace('_', ' ').title()

    def save(self, commit=True):
        profile = super().save(commit=False)

        if self.request_user and profile.user == self.request_user:
            try:
                old_profile = Profile.objects.get(pk=profile.pk)
                if old_profile.profile_picture and old_profile.profile_picture != profile.profile_picture:
                    old_path = old_profile.profile_picture.path
                    if os.path.isfile(old_path):
                        os.remove(old_path)
            except Profile.DoesNotExist:
                pass

        if commit:
            profile.save()
        return profile