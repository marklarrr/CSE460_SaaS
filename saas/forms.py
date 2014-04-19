from django import forms
from saas.models import UserProfile, Tenant, Worker
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ( 'addproject', 'addRequirements','modifyProjectStatus', 'viewReqStatus',
        			'viewProjectsManager', 'modReqStatus', 'viewAssignedReqs',)

