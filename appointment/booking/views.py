from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm
from .forms import ForgotPasswordForm  # Make sure to import your form
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from .models import Appointment, User,Office
from django.utils.timezone import now
from .forms import AppointmentForm, UserForm
from .forms import DocumentUploadForm
from .models import Document
from django.http import HttpResponse
# Assuming you have a form for handling this
from .forms import MissingIDCardForm
from .forms import ContactUsForm
from django.core.mail import send_mail
from django.conf import settings  # try to access email backend
from .models import Notification
from django.db.models import Count
from django.utils import timezone
import calendar
from .forms import UserForm
from .models import MissingIDCard
from django.views.generic import TemplateView
from campay.sdk import Client as CamPayClient
from django.http import JsonResponse
from django.core.serializers import serialize
import json
import yagmail

# Replace with your Gmail credentials
username = "kamsonganderson39@gmail.com"
password = "zbci mysk xhds gjxe"

# Create a yagmail object
yag = yagmail.SMTP(username, password)




User = get_user_model()
campay = CamPayClient({
    "app_username": "JByBUneb4BceuEyoMu1nKlmyTgVomd-QfokOrs4t4B9tPJS7hhqUtpuxOx5EQ7zpT0xmYw3P6DU6LU0mH2DvaQ",
    "app_password": "m-Xuj9EQIT_zeQ5hSn8hLjYlyJT7KnSTHABYVp7tKeHKgsVnF0x6PEcdtZCVaDM0BN5mX-eylX0fhrGGMZBrWg",
    "environment": "PROD"  # use "DEV" for demo mode or "PROD" for live mode
})


def home(request):
    return render(request, 'booking/home.html')


def register(request):
    if request.method == 'POST':
        print(request.POST)
        form = CustomUserCreationForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        print(request.POST)
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
                send_mail(mail_subject, message,
                          'your_email@example.com', [email])
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
    print("post inner1")
    if request.method == 'POST':
        print(request.POST)
        print(request.user)
        # Replace with actual user retrieval
        user_id = request.user.id
        user = User.objects.get(pk=user_id)
        officer = None  # Assuming officer can be null
        # Replace with actual office retrieval
        office = Office.objects.create(
            name="Mendong Office",
            address="mendong"
        )
        date = request.POST.get('date')
        time = "8:00"

        # user = User.objects.create(
        #     address="Mendong",
        #     name="Anderson1"
        # )
        # # user.save()
        print(office)
        # Create the appointment object
        appointment = Appointment.objects.create(
            user=user,
            officer=officer,
            office=office,
            date=date,
            time=time,
        )
        # appointment.save
        context = {}
        return render(request, 'panel/user/payment_page.html', context)
        # form = AppointmentForm(request.POST)
        # if form.is_valid():
        #     appointment = form.save(commit=False)
        #     # Additional processing logic as needed
        #     appointment.save()
        #     # Redirect to user panel or another appropriate view
        #     # return redirect('user_panel')

        # else:
        #     print(form.errors)  # Check form errors in console for debugging
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
            form = AppointmentForm()
            # Redirect to the payment page
            return render(request, 'panel/user/book_appointment.html', {'form': form})
        else:
            return HttpResponse("Error uploading documents. Please try again.")
    else:
        form = DocumentUploadForm()
        return render(request, 'panel/user/upload_document.html', {'form': form})

# @login_required


def payment_page(request):
    if request.method == 'POST':
        print(request.POST.get("phone"))
        collect = campay.collect({
            "amount": "3000",  # The amount you want to collect
            "currency": "XAF",
            # Phone number to request amount from. Must include country code
            "from": "237" + request.POST.get("phone"),
            "description": "fees for ID Card Creation",
            # Reference from the system initiating the transaction.
            "external_reference": "",
        })
        print(collect)
        if collect.get('status') == 'SUCCESSFUL':
            payment_data = {
                'reference': collect.get('reference'),
                'external_reference': collect.get('external_reference'),
                'status': collect.get('status'),
                'amount': collect.get('amount'),
                'currency': collect.get('currency'),
                'operator': collect.get('operator'),
                'code': collect.get('code'),
                'operator_reference': collect.get('operator_reference'),
                'description': collect.get('description'),
                'external_user': collect.get('external_user'),
                'reason': collect.get('reason'),
                'phone_number': collect.get('phone_number')

            }
            context = {'payment_info': payment_data}
            return render(request, 'panel/user/payment_success.html', context)
        else:
            if collect.get('reason'):
                context = {'message': collect.get('reason')}
                return render(request, 'panel/user/payment_page.html', context)
            elif collect.get('message'):
                context = {'message': collect.get('message')}
                return render(request, 'panel/user/payment_page.html', context)
            else:
                context = {
                    'message': 'An error occur with the payment please try later'}
                return render(request, 'panel/user/payment_page.html', context)

    else:
        context = {}
        return render(request, 'panel/user/payment_page.html', context)

@login_required
def track_application(request):
    return render(request, 'panel/user/track_application.html')

@login_required
def security_settings(request):
    return render(request, 'panel/user/security_settings.html')


@login_required
def insert_missing_id_card(request):
    if request.method == 'POST':
        form = MissingIDCardForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('user_panel')
    else:
        form = MissingIDCardForm()

    found_id_cards = MissingIDCard.objects.all()

    return render(request, 'panel/user/insert_missing_id_card.html', {'form': form, 'found_id_cards': found_id_cards})


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

            # Replace with your success template
            return render(request, 'contact_us_success.html')
    else:
        form = ContactUsForm()

    return render(request, 'contact_us.html', {'form': form})

 # police view


# @login_required
# def manage_appointments(request):
#     if request.user.role != 'officer':
#         return render(request, '403.html', status=403)

#     appointments = Appointment.objects.all()
#     print("appointments")
#     return render(request, 'panel/police/manage_appointments.html', {'appointments': appointments})


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


# notifier

@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user)

    # Gather data for chart
    current_year = timezone.now().year
    monthly_notifications = Notification.objects.filter(created_at__year=current_year).values(
        'created_at__month').annotate(count=Count('id')).order_by('created_at__month')

    notification_labels = [
        calendar.month_name[i['created_at__month']] for i in monthly_notifications]
    notification_counts = [i['count'] for i in monthly_notifications]

    context = {
        'notifications': notifications,
        'notification_labels': notification_labels,
        'notification_counts': notification_counts,
    }

    return render(request, 'panel/police/notifications.html', context)


# admin view

def manage_users(request):
    users = User.objects.all()
    return render(request, 'panel/admin/manage_users.html', {'users': users})


def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_users')
    else:
        form = UserForm()
    return render(request, 'panel/admin/add_user.html', {'form': form})


def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('manage_users')
    else:
        form = UserForm(instance=user)
    return render(request, 'panel/admin/edit_user.html', {'form': form})


def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('manage_users')


def manage_appointments(request):
    appointments = Appointment.objects.all()
    print(appointments)
    return render(request, 'panel/admin/manage_appointments.html', {'appointments': appointments})


def approve_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = 'Approved'
    appointment.save()
    print(appointment.user)
    # Compose and send an email
    subject = "appointment approved"
    body = "Your appointment have be approved"
    recipients = ["kamsonganderson39@gmail.com"]

    yag.send(to=recipients, subject=subject, contents=body)

    return redirect('manage_appointments')


def reject_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = 'Rejected'
    appointment.save()
    subject = "appointment rejected"
    body = "Your appointment have be rejected"
    recipients = ["kamsonganderson39@gmail.com"]
    return redirect('manage_appointments')


def manage_documents(request):
    documents = Document.objects.all()
    return render(request, 'panel/admin/manage_documents.html', {'documents': documents})


def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    document.delete()
    return redirect('manage_documents')


class AboutUsView(TemplateView):
    template_name = 'panel/admin/about_us.html'
