from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, TransporterProfile, Requirement, Bid

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=UserProfile.USER_TYPE_CHOICES)
    
    contact_number = forms.CharField(max_length=15, required=False)
    transporter_name = forms.CharField(max_length=255, required=False)
    vehicle_number = forms.CharField(max_length=50, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        user_type = cleaned_data.get("user_type")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        
        if user_type == 'Transporter':
            if not cleaned_data.get('transporter_name'):
                self.add_error('transporter_name', 'Transporter Name is required.')
            if not cleaned_data.get('vehicle_number'):
                self.add_error('vehicle_number', 'Vehicle Number is required.')
            
        return cleaned_data

class RequirementForm(forms.ModelForm):
    class Meta:
        model = Requirement
        fields = ['source_city', 'destination_city']

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
