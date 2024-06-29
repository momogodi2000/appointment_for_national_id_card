from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm
from .forms import ForgotPasswordForm  # Make sure to import your form
from django.contrib.sites.shortcuts import get_current_site


User = get_user_model()

def home(request):
    return render(request, 'booking/home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if user.role == 'admin':
                return redirect('admin_panel')
            elif user.role == 'officer':
                return redirect('officer_panel')
            else:
                return redirect('user_panel')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})


def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

            if user:
                current_site = get_current_site(request)
                mail_subject = 'Reset your password'
                message = render_to_string('password_reset_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                send_mail(mail_subject, message, 'your_email@example.com', [email])
            return redirect('password_reset_done')
    else:
        form = ForgotPasswordForm()
    
    return render(request, 'auth/forgot_password.html', {'form': form})

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home')

@login_required
def user_panel(request):
    return render(request, 'panel/user_panel.html')

@login_required
def officer_panel(request):
    return render(request, 'panel/officer_panel.html')

@login_required
def admin_panel(request):
    return render(request, 'panel/admin_panel.html')
