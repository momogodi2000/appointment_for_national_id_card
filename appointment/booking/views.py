from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, RegistrationForm
from .forms import ForgotPasswordForm  # Make sure to import your form
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.http import FileResponse
from .models import Appointment, User,Office
from django.utils.timezone import now
from .forms import AppointmentForm, UserForm
from .forms import DocumentUploadForm
from .forms import *
from .models import Document
from django.http import HttpResponse
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
# Assuming you have a form for handling this
from .forms import MissingIDCardForm
from .forms import ContactUsForm
from reportlab.pdfgen import canvas
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
from rest_framework.views import APIView

# Replace with your Gmail credentials
username = "kamsonganderson39@gmail.com"
password = "zbci mysk xhds gjxe"

# Create a yagmail object
yag = yagmail.SMTP(username, password)

def generate_pdf_file(
    payment_receipt_info
):
    from io import BytesIO

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    current_user = payment_receipt_info["user"]

    # Create a PDF document
    p.drawString(100, 750, "Payment Receipt For National ID Card Establishment")

    y = 700
    for i in range(1):
        p.drawString(100, y, f"Reference: {payment_receipt_info['reference']}")
        p.drawString(100, y - 20, f"ID: {payment_receipt_info['reference']}")
        p.drawString(100, y - 40, f"User: {current_user.username}")
        p.drawString(100, y - 60, f"Phone Number: {payment_receipt_info['from']}")
        p.drawString(100, y - 80, f"Fees: {payment_receipt_info['amount']}{payment_receipt_info['currency']}")
        p.drawString(100, y - 100, f"Police station: {payment_receipt_info['location']}")
        p.drawString(100, y - 120, f"Description: {payment_receipt_info['description']}")
        p.drawString(100, y - 140, f"Date: {payment_receipt_info['date']}")
        y -= 60

    qrcode_info = {
        f"Reference: {payment_receipt_info['reference']}",
        f"ID: {payment_receipt_info['reference']}",
        f"User: {current_user.username}",
        f"Phone Number: {payment_receipt_info['from']}",
        f"Fees: {payment_receipt_info['amount']}{payment_receipt_info['currency']}",
        f"Police station: {payment_receipt_info['location']}",
        f"Description: {payment_receipt_info['description']}",
        f"Date: {payment_receipt_info['date']}"
    }

    qrw = QrCodeWidget(str(qrcode_info))
    b = qrw.getBounds()
    w=b[2] - b[0]
    h=b[3] - b[1]
    d = Drawing(400, 400, transform=[45./w,0,0,56./h,0,0])
    d.add(qrw)
    renderPDF.draw(d, p, 1, 1)
    print(f"QR CODE INFO : {qrw.value}")

    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer


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
        form = RegistrationForm()
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

def get_documents(request, user_id):
    document_links = Document.objects.get(user=user_id)
    return render(request, "panel/police/view_docs.html", {"documents":document_links})

def payment_page(request):
    if request.method == 'POST':
        collect = campay.collect({
            "amount": "10",  # The amount you want to collect
            "currency": "XAF",
            # Phone number to request amount from. Must include country code
            "from": "237" + request.POST.get("phone"),
            "description": "NATIONAL ID CARD FEES",
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
            payment_receipt_info = {
            "amount": "10",  # The amount you want to collect
            "currency": "XAF",
            "user": request.user,
            "date": now(),
            'reference': collect.get('reference'),
            'external_reference': collect.get('external_reference'),
            # Phone number to request amount from. Must include country code
            "from": "237" + request.POST.get("phone"),
            "description": "NATIONAL ID CARD FEES",
            "location": "Mendong"
            }
            userAppointment = Appointment.objects.get(user=request.user.id)
            print(f"User appointments: {userAppointment}")
            userAppointment.paid = True
            userAppointment.save()
            buffer = generate_pdf_file(payment_receipt_info)
            context = {'payment_info': payment_data, "buffer": buffer}
            response = FileResponse(buffer, as_attachment=True, filename='mypdf.pdf', content_type='application/pdf')
            response.headers['Content-Disposition'] = 'inline; filename= "mypdf.pdf"'
            response.headers['Content-Type'] = 'application/pdf'
            return response
            # return render(request, 'panel/user/payment_success.html', context)
        else:
            userAppointment = Appointment.objects.get(user=request.user.id)
            userAppointment.paid = False
            userAppointment.save()
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
    if request.method == 'POST':
        application_id = request.POST.get("applicationId")
        if application_id:
            try:
                appointment = Appointment.objects.get(id=application_id)
                status = appointment.card_status
                return render( request , "panel/user/card_status.html", {'status': status})
            except Appointment.DoesNotExist:
                return render( request , "panel/user/card_status.html", {'status': 'Appointment id not found'})
        else:
            return render( request , "panel/user/card_status.html", {'status': 'Invalid appointment id'})
    return render(request, 'panel/user/track_application.html')


@login_required
def security_settings(request):
    if request.method == 'POST':
        current_password = request.POST.get('currentPassword')
        new_password = request.POST.get('newPassword')
        confirm_password = request.POST.get('confirmPassword')

        if not request.user.check_password(current_password):
            context = {'error': 'Current password is incorrect'}
        elif new_password != confirm_password:
            context = {'error': 'New passwords do not match'}
        else:
            request.user.set_password(new_password)
            request.user.save()
            context = {'success': 'Password updated successfully'}
    else:
        context = {}

    return render(request, 'panel/user/security_settings.html', context)


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
            form.save()
            # Send email
            # send_mail(
            #     'Contact Form Submission',
            #     f'Name: {name}\nEmail: {email}\nMessage: {message}',
            #     settings.DEFAULT_FROM_EMAIL,
            #     [settings.DEFAULT_FROM_EMAIL],
            # )

            # Replace with your success template
            return render(request, 'panel/user/contact_us_success.html')
        else:
            print(f"Error: {form.errors}")
            return redirect("contact_us")

    else:
        form = ContactUsForm()
        return render(request, 'panel/user/contact_us.html', {'form': form})

 # police view


# @login_required
# def manage_appointments(request):
#     if request.user.role != 'officer':
#         return render(request, '403.html', status=403)

#     appointments = Appointment.objects.all()
#     print("appointments")
#     return render(request, 'panel/police/manage_appointments.html', {'appointments': appointments})


@login_required
def communication_form(request):
    if request.method == "GET":
        form = CommunicationUploadForm()
        return render(request, "panel/police/add_communication.html", {"form": form})
    else:
        form = CommunicationUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("communications")
        else:
            print(form.errors)
            return redirect("communication_form")
        
@login_required
def communications(request):
    if (request.method=="GET"):
        communications = Communication.objects.all()
        return render(request, "panel/police/communication.html", {"communications": communications})

@login_required
def admin_communications(request):
    if (request.method=="GET"):
        communications = Communication.objects.all()
        return render(request, "panel/admin/communications.html", {"communications": communications})
    
@login_required
def user_communications(request):
    communications = Communication.objects.all()
    return render(request, "panel/user/communication.html", {"communications": communications})
    
@login_required
def card_status(request):
    if (request.method=="GET"):
        communications = Appointment.objects.all()
        return render(request, "panel/police/card_status.html", {"cards": communications})

@login_required
def edit_card_status(request, id):
    appointment = Appointment.objects.get(pk=id)
    if request.method == "GET":
        form = EditCardStatusForm(instance=appointment)
        return render(request, "panel/police/edit_card_status.html", {"form": form})

    else:
        form = EditCardStatusForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
        return redirect("card_status")

@login_required
def contact_messages(request):
    contact_us =  ContactUs.objects.all()
    return render(request, "panel/admin/contact_us.html", {"contact":contact_us})

@login_required
def edit_communication(request, id):
    communication = get_object_or_404(Communication, pk=id)
    if request.method == "POST":
        form = CommunicationUploadForm(request.POST, instance=communication)
        if form.is_valid():
            form.save()
            return redirect('communications')
    else:    
        single_communication = Communication.objects.get(pk=id)
        form = CommunicationUploadForm(instance=single_communication)
        return render(request,"panel/police/edit_communication.html", {"form": form})
    
@login_required
def delete_communication(request, id):
    communication = get_object_or_404(Communication, pk=id)
    communication.delete()
    return redirect("communications")

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
    notifications = Notification.objects.filter(appointment=request.user.id)

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


def admin_edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('manage_users')
    else:
        form = UserForm(instance=user)
    return render(request, 'panel/admin/edit_user.html', {'form': form})


def admin_delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('manage_users')


def manage_appointments(request):
    appointments = Appointment.objects.all()
    return render(request, 'panel/police/manage_appointments.html', {'appointments': appointments})

def admin_manage_appointments(request):
    appointments = Appointment.objects.all()
    return render(request, 'panel/admin/manage_appointments.html', {'appointments': appointments})

def approve_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    # appointment.status = 'approved'
    # appointment.save()
    print(appointment.user)
    citizen = User.objects.get(username=appointment.user)
    # Compose and send an email
    subject = "Appointment approved"
    body = "Your appointment has been approved"
    recipients = [f"{citizen.email}"]

    yag.send(to=recipients, subject=subject, contents=body)

    return redirect('manage_appointments')


def reject_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = 'rejected'
    citizen = User.objects.get(username=appointment.user)
    appointment.save()
    subject = "Appointment rejected"
    body = "Your appointment have be rejected"
    recipients = [f"{citizen.email}"]
    yag.send(to=recipients, subject=subject, contents=body)
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