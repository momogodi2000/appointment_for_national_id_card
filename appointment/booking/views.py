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
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI
from .models import User, Appointment, Document, MissingIDCard, Notification, Communication, ContactUs
from django.core.files.storage import default_storage



client = OpenAI(api_key=settings.OPENAI_API_KEY)
import os





# Replace with your Gmail credentials
username = "yvangodimomo@gmail.com"
password = "pzls apph esje cgdl"

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


def activation_code_email(request):
    if request.method == 'GET':
        return render(request, "auth/activation_code_email.html")
    else:
        user = None
        try:
            user = User.objects.get(email=request.POST["email"])
        except Exception as e:
            pass
        if user is None:
            return render(request, "auth/password_reset_success.html", {"status":400, "message": "Invalid email"})
        password_reset = None
        try:
            password_reset = PasswordReset.objects.get(code=request.POST["code"], user=user.pk)
        except Exception as e:
            pass
        if password_reset is None:
            return render(request, "auth/password_reset_success.html", {"status":400, "message": "Invalid acrivation code"})
        data_without_email = {
            "code": request.POST["code"],
            "user": user.pk
        }
        reset_form = PasswordResetForm(data=data_without_email)
        if reset_form.is_valid():
            hashedPassword = make_password(request.POST["new_password"])
            user.password = hashedPassword
            user.save()
            return render(request, "auth/password_reset_success.html", {"status":200, "message": "Password reset successful !"})
        return render(request, "auth/password_reset_success.html", {"status":400, "message": "An error occurred !"})

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
                random_string = get_random_string(6)
                mail_subject = 'Reset your password'
                recepients = [f"{user.email}"]
                message = f"Enter the activation code to proceed {random_string}"
                yag.send(to=recepients, subject=mail_subject, contents=message)
                password_reset = None
                try:
                    password_reset = PasswordReset.objects.get(user = user.pk)
                except Exception as e:
                    pass
                if password_reset is None:
                    data = {
                        "code": random_string,
                        "user": user.pk
                    }
                    form = PasswordResetForm(data=data)
                    if form.is_valid():
                        form.save()
                else:
                    password_reset.code = random_string
                    password_reset.save()
                return render(request, "auth/activation_code_email.html", {"user":user})
            return redirect('forgot_password')
        return redirect('forgot_password')
        
    else:
        form = ForgotPasswordForm()

    return render(request, 'auth/forgot_password.html', {'form': form})



@login_required
def logout(request):
    auth_logout(request)
    return redirect('home')


##police panel

@login_required
def officer_panel(request):
     # Count the instances of each model
    user_count = User.objects.count()
    appointment_count = Appointment.objects.count()
    document_count = Document.objects.count()
    missing_id_card_count = MissingIDCard.objects.count()
    notification_count = Notification.objects.count()
    communication_count = Communication.objects.count()
    contact_us_count = ContactUs.objects.count()

    # Fetch region data
    regions = Office.objects.all()

    # Example regions data (you can replace this with real data if applicable)
    regions = [
    {'name': 'Adamaoua', 'headquarter': 'Ngaoundéré', 'population': 1124000},
    {'name': 'Centre', 'headquarter': 'Yaoundé', 'population': 3905000},
    {'name': 'East', 'headquarter': 'Bertoua', 'population': 830000},
    {'name': 'Far North', 'headquarter': 'Maroua', 'population': 3796000},
    {'name': 'Littoral', 'headquarter': 'Douala', 'population': 3178000},
    {'name': 'North', 'headquarter': 'Garoua', 'population': 1703000},
    {'name': 'Northwest', 'headquarter': 'Bamenda', 'population': 1735000},
    {'name': 'South', 'headquarter': 'Ebolowa', 'population': 641000},
    {'name': 'Southwest', 'headquarter': 'Buea', 'population': 1720047},
    {'name': 'West', 'headquarter': 'Bafoussam', 'population': 2510283}
]


   # Render the template with the counts and regions
    return render(request, 'panel/officer_panel.html', {
        'user_count': user_count,
        'appointment_count': appointment_count,
        'document_count': document_count,
        'missing_id_card_count': missing_id_card_count,
        'notification_count': notification_count,
        'communication_count': communication_count,
        'contact_us_count': contact_us_count,
        'regions': regions
    })


@login_required
def admin_panel(request):
       # Count the instances of each model
    user_count = User.objects.count()
    appointment_count = Appointment.objects.count()
    document_count = Document.objects.count()
    missing_id_card_count = MissingIDCard.objects.count()
    notification_count = Notification.objects.count()
    communication_count = Communication.objects.count()
    contact_us_count = ContactUs.objects.count()

    # Fetch region data
    regions = Office.objects.all()


   # Render the template with the counts and regions
    return render(request, 'panel/admin_panel.html', {
        'user_count': user_count,
        'appointment_count': appointment_count,
        'document_count': document_count,
        'missing_id_card_count': missing_id_card_count,
        'notification_count': notification_count,
        'communication_count': communication_count,
        'contact_us_count': contact_us_count,
        'regions': regions
    })


#clients panel


@login_required
def user_panel(request):
    return render(request, 'panel/user_panel.html')

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
        office = Office.objects.create(
            name="Mendong Office",
            address="mendong"
        )
        date = request.POST.get('date')
        time = "8:00"


        print(office)
        appointment = Appointment.objects.create(
            user=user,
            officer=officer,
            office=office,
            date=date,
            time=time,
        )

        context = {}
        return render(request, 'panel/user/payment_page.html', context)

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

            return render(request, 'panel/user/book_appointment.html', {'form': form})
        else:
            return HttpResponse("Error uploading documents. Please try again.")
    else:
        form = DocumentUploadForm()
        return render(request, 'panel/user/upload/upload_document.html', {'form': form})

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

from django.core.files.storage import FileSystemStorage


@login_required
def security_settings(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        current_password = request.POST.get('currentPassword')
        new_password = request.POST.get('newPassword')
        confirm_password = request.POST.get('confirmPassword')
        profile_picture = request.FILES.get('profile_picture')

        # Update name and email
        request.user.name = name
        request.user.email = email

        # Check current password for security
        if not request.user.check_password(current_password):
            context = {'error': 'Current password is incorrect'}
        else:
            # Update password if provided and valid
            if new_password and new_password == confirm_password:
                request.user.set_password(new_password)

            # Update profile picture if provided
            if profile_picture:
                request.user.profile_picture = profile_picture

            request.user.save()
            context = {'success': 'Settings updated successfully'}
            # Redirect to avoid resubmission on refresh
            return redirect('user_panel')
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
            # Replace with your success template
            return render(request, 'panel/user/contact_us_success.html')
        else:
            print(f"Error: {form.errors}")
            return redirect("contact_us")

    else:
        form = ContactUsForm()
        return render(request, 'panel/user/contact_us.html', {'form': form})


@login_required
def history(request):
    return render(request, 'panel/user/support/history.html')

@login_required
def about(request):
    return render(request, 'panel/user/support/about.html')




# Set your OpenAI API key

@login_required
def support_discussion(request):
    return render(request, 'panel/user/support/support_discussion.html')

@csrf_exempt
def get_bot_response(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        try:
            response = client.chat.completions.create(model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant specialized in Cameroonian national ID card delivery and administrative matters. Provide concise and accurate information."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=150,
            temperature=0.5)
            bot_reply = response.choices[0].message.content.strip()
            return JsonResponse({'reply': bot_reply})
        except Exception as e:
            print(f"OpenAI API Error: {e}")
            return JsonResponse({'reply': "I'm sorry, something went wrong while processing your request. Please try again later."}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


def security_grade(request):
    return render(request, 'panel/user/grade/security_grade.html')





def view_detail(request, grade):
    grades_info = {
      'national_police': {
        'title': 'National Police',
        'description': 'The National Police is responsible for maintaining public order and safety in urban areas. They manage day-to-day law enforcement activities, address crime-related issues, and ensure the enforcement of local laws. Officers in this force work in cities and towns, handling a wide range of incidents from traffic violations to serious crimes.',
        'image': 'img/national_police.jpeg',
    },
    'judicial_police': {
        'title': 'Judicial Police',
        'description': 'The Judicial Police, also known as the judicial branch of the police, specializes in criminal investigations and the enforcement of judicial orders. They play a critical role in gathering evidence, conducting interviews, and working closely with the judiciary to ensure that criminal cases are thoroughly investigated and prosecuted. Their work often involves collaboration with other law enforcement agencies and legal professionals.',
        'image': 'img/judicial_police.jpeg',
    },
    'gendarmerie': {
        'title': 'National Gendarmerie',
        'description': 'The National Gendarmerie is a paramilitary force that combines military and police duties. It operates in rural areas, borders, and regions with high security concerns. The gendarmerie is tasked with maintaining public order, securing national borders, and providing assistance in areas where the National Police might not have a strong presence. Their responsibilities include counter-terrorism, anti-smuggling operations, and crowd control.',
        'image': 'img/gendarmerie.jpeg',
    },
    'assistant_police': {
        'title': 'Assistant Police',
        'description': 'Assistant Police officers play a supervisory role, overseeing a team of police officers and ensuring the effective execution of their duties. They provide guidance, support, and management to junior officers, handle administrative tasks, and coordinate responses to incidents. Their role is crucial in maintaining discipline and efficiency within their teams and ensuring that operations are conducted smoothly.',
        'image': 'img/assistant.jpeg',
    },
    'sergeant': {
        'title': 'Sergeant',
        'description': 'Sergeants hold a leadership position within the police force, responsible for managing a larger team and providing tactical leadership during operations. They oversee the implementation of strategies, supervise junior officers, and ensure that their team follows proper procedures and protocols. Sergeants are often involved in training new recruits, handling complex cases, and coordinating with other units to achieve operational goals.',
        'image': 'img/sergeant.jpeg',
    },
    'inspector': {
        'title': 'Inspector',
        'description': 'Inspectors are experienced officers who investigate crimes, supervise lower ranks, and manage specific units or divisions. They are involved in detailed casework, including analyzing evidence, conducting interviews, and liaising with other law enforcement agencies. Inspectors also play a role in strategic planning, policy development, and ensuring that investigations are conducted in accordance with legal standards.',
        'image': 'img/ip.jpeg',
    },
    'senior_inspector': {
        'title': 'Senior Inspector',
        'description': 'Senior Inspectors lead major investigations, manage specialized units, and report to higher-ranking officers. They are responsible for overseeing complex and high-profile cases, coordinating with other departments, and ensuring that investigative strategies are effective and aligned with organizational objectives. Senior Inspectors also contribute to policy development and strategic planning within the police force.',
        'image': 'img/so.jpeg',
    },
    'police_officer': {
        'title': 'Police Officer',
        'description': 'Police Officers are responsible for maintaining law and order, responding to emergencies, and performing various law enforcement duties. They may hold leadership positions such as company commander or station chief, overseeing the operations of their unit and ensuring that policies and procedures are followed. Police Officers engage directly with the community, address concerns, and enforce laws to ensure public safety.',
        'image': 'img/police2.jpeg',
    },
    'commissioner': {
        'title': 'Commissioner',
        'description': 'Commissioners oversee large units or departments within the police force, including districts or specialized divisions. They are responsible for strategic planning, resource allocation, and ensuring that their units achieve operational objectives. Commissioners work closely with other senior officers, government officials, and community leaders to address major issues, develop policies, and implement initiatives to enhance public safety.',
        'image': 'img/tenue.jpeg',
    },
    'general_inspector': {
        'title': 'General Inspector',
        'description': 'The General Inspector is the highest rank in the National Police, responsible for national security operations and overall strategic direction. They oversee the entire police force, coordinate with other national and international agencies, and ensure the effective implementation of security policies and procedures. The General Inspector plays a key role in shaping national security strategies, addressing major security challenges, and representing the police force at the highest levels.',
        'image': 'img/cyber.jpeg',
    },
}

    grade_info = grades_info.get(grade)
    return render(request, 'panel/user/grade/view_detail.html', {'grade': grade_info})


def center(request):
    return render(request, 'panel/user/grade/center.html')


# police view


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




def manage_contact(request):
    contacts = ContactUs.objects.all()
    return render(request, 'panel/police/manage_contact/manage_contact.html', {'contacts': contacts})

def reply_contact(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        message = request.POST.get('message')
        send_mail(
            'Reply to Your Contact Message',
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        return redirect('manage_contact')

def delete_contact(request, contact_id):
    contact = ContactUs.objects.get(id=contact_id)
    contact.delete()
    return redirect('manage_contact')



def manage_id(request):
    missing_id_cards = MissingIDCard.objects.all()
    return render(request, 'panel/police/manage_id/manage_id.html', {'missing_id_cards': missing_id_cards})

def add_missing_id_card(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        id_card_image = request.FILES.get('id_card_image')
        MissingIDCard.objects.create(
            name=name,
            email=email,
            phone=phone,
            id_card_image=id_card_image
        )
        return redirect('manage_id')

def delete_id_card(request, id_card_id):
    id_card = MissingIDCard.objects.get(id=id_card_id)
    default_storage.delete(id_card.id_card_image.name)  # Delete the image from storage
    id_card.delete()
    return redirect('manage_id')





# admin view

def manage_users(request):
    users = User.objects.all()
    return render(request, 'panel/admin/manage_user/manage_users.html', {'users': users})


def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_users')
    else:
        form = UserForm()
    return render(request, 'panel/admin/manage_user/add_user.html', {'form': form})


def admin_edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('manage_users')
    else:
        form = UserForm(instance=user)
    return render(request, 'panel/admin/manage_user/edit_user.html', {'form': form})


def admin_delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('manage_users')


def manage_appointments(request):
    appointments = Appointment.objects.all()
    return render(request, 'panel/admin/appoitment/manage_appointments.html', {'appointments': appointments})

def admin_manage_appointments(request):
    appointments = Appointment.objects.all()
    return render(request, 'panel/admin/appoitment/manage_appointments.html', {'appointments': appointments})

def approve_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

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
    return render(request, 'panel/admin/manage_doc/manage_documents.html', {'documents': documents})


def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    document.delete()
    return redirect('manage_documents')


class AboutUsView(TemplateView):
    template_name = 'panel/admin/about/about_us.html'

def map_view(request):
    return render(request, 'panel/admin/map/map.html')


from django.shortcuts import render
from django.db.models import Count, Avg
from datetime import timedelta, date
from .models import User, Appointment

@login_required
def analyse_view(request):
# User Role Distribution
    role_distribution = User.objects.values('role').annotate(count=Count('role')).order_by('role')
    role_data = [item['count'] for item in role_distribution]
    
    # Appointment Status Distribution
    status_distribution = Appointment.objects.values('status').annotate(count=Count('status')).order_by('status')
    status_data = [item['count'] for item in status_distribution]

    # Average Appointments per Officer
    avg_appointments = Appointment.objects.values('officer').annotate(avg_appointments=Count('id')).aggregate(avg_officer_appointments=Avg('avg_appointments'))['avg_officer_appointments']

    # 6-month Estimation for appointments
    today = date.today()
    six_months_ago = today - timedelta(days=180)
    six_month_appointments = Appointment.objects.filter(date__gte=six_months_ago).count()
    
    # Other statistics can be added here as necessary (e.g., user registration growth)

    context = {
        'role_distribution': role_data,
        'status_distribution': status_data,
        'avg_appointments': avg_appointments,
        'six_month_appointments': six_month_appointments,
    }

    return render(request, 'panel/admin/analyse/analyse.html', context)