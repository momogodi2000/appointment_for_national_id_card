from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm
from .forms import ForgotPasswordForm  # Make sure to import your form
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from .models import Appointment, User
from django.utils.timezone import now
from .forms import AppointmentForm, UserForm
from .forms import DocumentUploadForm
from .models import Document
from django.http import HttpResponse
from .forms import MissingIDCardForm  # Assuming you have a form for handling this
from .forms import ContactUsForm
from django.core.mail import send_mail
from django.conf import settings      #try to access email backend
from .models import Notification
from django.db.models import Count
from django.utils import timezone
import calendar
from .forms import UserForm 






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



@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            # Additional processing logic as needed
            appointment.save()
            return redirect('user_panel')  # Redirect to user panel or another appropriate view
        else:
            print(form.errors)  # Check form errors in console for debugging
    else:
        form = AppointmentForm()
    return render(request, 'panel/user/book_appointment.html', {'form': form})



@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            return HttpResponse("Documents uploaded successfully")
        else:
            return HttpResponse("Error uploading documents. Please try again.")
    else:
        form = DocumentUploadForm()
    return render(request, 'panel/user/upload_document.html', {'form': form})


def track_application(request):
    return render(request, 'panel/user/track_application.html')

def security_settings(request):
    return render(request, 'panel/user/security_settings.html')



def insert_missing_id_card(request):
    if request.method == 'POST':
        form = MissingIDCardForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the form data
            form.save()
            # Optionally, redirect to a success page or back to the dashboard
            return redirect('user_panel')  # Replace with your dashboard URL name
    else:
        form = MissingIDCardForm()
    
    return render(request, 'panel/user/insert_missing_id_card.html', {'form': form})


def contact_us(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Send email
            send_mail(
                'Contact Form Submission',
                f'Name: {name}\nEmail: {email}\nMessage: {message}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
            )

            return render(request, 'contact_us_success.html')  # Replace with your success template
    else:
        form = ContactUsForm()

    return render(request, 'contact_us.html', {'form': form})

 #police view


@login_required
def manage_appointments(request):
    if request.user.role != 'officer':
        return render(request, '403.html', status=403)

    appointments = Appointment.objects.all()
    return render(request, 'panel/police/manage_appointments.html', {'appointments': appointments})

@login_required
def user_information(request):
    users = User.objects.all()
    return render(request, 'panel/police/user_information.html', {'users': users})

@login_required
def edit_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == "POST":
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('manage_appointments')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'panel/police/edit_appointment.html', {'form': form})

@login_required
def delete_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.delete()
    return redirect('manage_appointments')

@login_required
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_information')
    else:
        form = UserForm(instance=user)
    return render(request, 'panel/police/edit_user.html', {'form': form})

@login_required
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        user.delete()
        return redirect('user_information')
    return render(request, 'panel/police/delete_user.html', {'user': user})


#notifier

@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user)

    # Gather data for chart
    current_year = timezone.now().year
    monthly_notifications = Notification.objects.filter(created_at__year=current_year).values('created_at__month').annotate(count=Count('id')).order_by('created_at__month')

    notification_labels = [calendar.month_name[i['created_at__month']] for i in monthly_notifications]
    notification_counts = [i['count'] for i in monthly_notifications]

    context = {
        'notifications': notifications,
        'notification_labels': notification_labels,
        'notification_counts': notification_counts,
    }

    return render(request, 'panel/police/notifications.html', context)