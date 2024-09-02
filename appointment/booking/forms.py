from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User as DefaultUser
from .models import User
from .models import Appointment
from .models import Document
from .models import MissingIDCard
from .models import *

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email' ,'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))

class CustomUserCreationForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = User
        # fields = UserCreationForm.Meta.fields + ('role',)
        fields = RegistrationForm.Meta.fields

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['user', 'date', 'time', 'status'] # Adjust fields as per your model definition



from django.core.exceptions import ValidationError

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document  # Replace with your actual model
        fields = [
            'birth_certificate', 
            'proof_of_nationality', 
            'passport_photos', 
            'residence_permit', 
            'marriage_certificate',
        ]
        widgets = {
            'birth_certificate': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'onchange': 'previewFile(this)'}),
            'proof_of_nationality': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'onchange': 'previewFile(this)'}),
            'passport_photos': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'onchange': 'previewFile(this)'}),
            'residence_permit': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'onchange': 'previewFile(this)'}),
            'marriage_certificate': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'onchange': 'previewFile(this)'}),
        }

    def __init__(self, *args, **kwargs):
        super(DocumentUploadForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False

    def clean(self):
        cleaned_data = super().clean()
        valid_types = ['image/jpeg', 'image/png', 'image/tiff']
        
        for field in self.fields:
            file = cleaned_data.get(field)
            if file:
                if file.content_type not in valid_types:
                    raise ValidationError(f'{field.replace("_", " ").title()} must be an image in JPG, JPEG, PNG, or TIFF format.')
        
        return cleaned_data



class MissingIDCardForm(forms.ModelForm):
    class Meta:
        model = MissingIDCard
        fields = ['name', 'email', 'phone', 'id_card_image']


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields =["name", "email", "message"]
    def __init__(self, *args, **kwargs):
        super(ContactUsForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'name', 'email', 'phone', 'address', 'role')

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class CommunicationUploadForm(forms.ModelForm):
    class Meta:
        model = Communication
        fields = ["title", "location"]
        widgets = {
            "location": forms.FileInput(attrs={"accept": '.pdf,.png,.jpg,.jpeg'})   
        }
    def __init__(self, *args, **kwargs):
        super(CommunicationUploadForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False

class EditCardStatusForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["id", "card_status"]
        widgets = {
            "id": forms.CharField(max_length=35),
            "card_status": forms.Select(attrs={"required": True}, choices=Appointment.CARD_CHOICES)
        }