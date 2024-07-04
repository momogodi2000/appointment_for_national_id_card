from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User as DefaultUser
from .models import User
from .models import Appointment
from .models import Document
from .models import MissingIDCard

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('role',)

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['user', 'date', 'time', 'status'] # Adjust fields as per your model definition



class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = [
            'birth_certificate', 
            'proof_of_nationality', 
            'passport_photos', 
            'residence_permit', 
            'marriage_certificate', 
            'death_certificate', 
            'sworn_statement'
        ]
        widgets = {
            'birth_certificate': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'onchange': 'previewFile(this)'}),
            'proof_of_nationality': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'onchange': 'previewFile(this)'}),
            'passport_photos': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'onchange': 'previewFile(this)'}),
            'residence_permit': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'onchange': 'previewFile(this)'}),
            'marriage_certificate': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'onchange': 'previewFile(this)'}),
            'death_certificate': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'onchange': 'previewFile(this)'}),
            'sworn_statement': forms.ClearableFileInput(attrs={'class': 'form-control-file', 'onchange': 'previewFile(this)'}),
        }

    def __init__(self, *args, **kwargs):
        super(DocumentUploadForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False



class MissingIDCardForm(forms.ModelForm):
    class Meta:
        model = MissingIDCard
        fields = ['name', 'email', 'phone', 'id_card_image']


class ContactUsForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

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