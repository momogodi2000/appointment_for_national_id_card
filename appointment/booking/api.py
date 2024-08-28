from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.http import FileResponse
from rest_framework.response import Response
from .models import Appointment, User,Office
from rest_framework.views import APIView
from django.utils.timezone import now
from django.http import HttpResponse
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
# Assuming you have a form for handling this
from reportlab.pdfgen import canvas
from django.core.mail import send_mail
import yagmail
from django.conf import settings  # try to access email backend
from .models import Notification
from django.db.models import Count
from django.utils import timezone
import calendar
from .models import *
from .serializers import *
from django.views.generic import TemplateView
from campay.sdk import Client as CamPayClient
from django.http import JsonResponse
from django.core.serializers import serialize
import json
import yagmail
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password, make_password
from django.utils.crypto import get_random_string
from rest_framework.authtoken.models import Token

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

class RegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        user = UserSerializer(data = request.data)
        if user.is_valid():
            user.save()
            return Response({"message": "User created successfully !"}, status=status.HTTP_201_CREATED)
        return Response({"message": user.errors}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        user = None
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            return Response({"message": "Invalid credentials !"}, status=status.HTTP_400_BAD_REQUEST)
        if not check_password(password, user.password):
            return Response(
                {"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
            )
        user_serializer = User()
        user_serializer.username = user.username
        user_serializer.password = password
        user_serializer.save()
        token, _ = Token.objects.get_or_create(user=user_serializer)
        return Response(
            {"data": UserSerializer(user).data, "token": token.key},
            status=status.HTTP_200_OK,
        )

class AppointmentView(APIView):
    def get(self, request):
        appointments = Appointment.objects.all()
        serialized_appointments = AppointmentSerializer(appointments, many=True)
        return Response({
            "data": serialized_appointments.data
        }, status = status.HTTP_200_OK)
    
    def post(self,request):
        appointment = AppointmentSerializer(data=request.data)
        if appointment.is_valid():
            appointment.save()
            return Response({
                "message": "Appointment booked successfully !"
            }, status=status.HTTP_200_OK)
        return Response({
            "messages": appointment.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self,request, appointmentId):
        appointment = Appointment.objects.get(pk = appointmentId)
        appointment_response = request.data.get("response")
        if not appointment:
            return Response({"message": f"Appointment not found !"}, status=status.HTTP_404_NOT_FOUND)
        
        appointment.status = appointment_response
        appointment.save()
        return Response({"message": f"Appointment {appointment_response} successfully !"}, status=status.HTTP_200_OK)

    def delete(self, request, appointmentId):
        appointment = Appointment.objects.get(pk=appointmentId)
        appointment.delete()
        return Response({"message": f"Appointment deleted successfully !"}, status=status.HTTP_200_OK)


class UserView(APIView):
    def get(self,request):
        users = User.objects.all()
        users_serialized = UserSerializer(users, many=True)
        return Response({"message": f"Users fetched successfully !", "data":users_serialized.data}, status=status.HTTP_200_OK)
    
    def post(self,request):
        user = UserSerializer(data=request.data)
        if user.is_valid():
            user.save()
            return Response({"message": f"User added successfully !"}, status=status.HTTP_201_CREATED)
        return Response({"message": user.errors}, status=status.HTTP_200_OK)

    def put(self, request, id):
        user = User.objects.get(pk=id)
        user_update = UserSerializer(user, data=request.data, partial=True)
        if user_update.is_valid():
            user_update.save()
            return Response({"message": f"User updated successfully !"}, status=status.HTTP_200_OK)
        return Response({"message": user_update.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        user = User.objects.get(pk=id)
        user.delete()
        return Response({"message": f"User deleted successfully !"}, status=status.HTTP_200_OK)
    

class MissingCardView(APIView):
    def get(self, request):
        missing_cards = MissingIDCard.objects.all()
        missing_cards_serializers = MissingIDCardSerializer(missing_cards, many=True)
        return Response({"message": f"Missing cards fetched successfully !", "data":missing_cards_serializers.data}, status=status.HTTP_200_OK)
        # else :
        #     return Response({"message": f"Missing cards fetched successfully !", "data":[]}, status=status.HTTP_200_OK)

    def post(self, request):
        missing_card = MissingIDCardSerializer(data=request.data)
        if missing_card.is_valid():
            missing_card.save()
            return Response({"message": f"Missing ID uploaded successfully !"}, status=status.HTTP_201_CREATED)
        return Response({"message": missing_card.errors}, status=status.HTTP_200_OK)

class CardStatusView(APIView):
    def get(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, pk=appointment_id)
        if appointment is not None:
            card_status = appointment.card_status
            return Response({"data": card_status}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Appointment not found"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, pk=appointment_id)
        response = request.data.get("response")
        if not appointment:
            return Response({"message": f"Appointment not found !"}, status=status.HTTP_404_NOT_FOUND)

        appointment.card_status = response
        appointment.save()
        return Response({"message": f"Card {response} successfully !"}, status=status.HTTP_200_OK)

class ContactUsView(APIView):
    def get(self, request):
        contacts = ContactUs.objects.all()
        serialized_contacts = ContactUsSerializer(contacts, many=True)
        # if serialized_contacts.is_valid():
        return Response({"message": f"Contact us messages fetched successfully !", "data":serialized_contacts.data}, status=status.HTTP_200_OK)
        # return Response({"message": serialized_contacts.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request):
        contact_us = ContactUsSerializer(data=request.data)
        if contact_us.is_valid():
            contact_us.save()
            return Response({"message": f"Message sent successfully !"}, status=status.HTTP_201_CREATED)
        return Response({"message": contact_us.errors}, status=status.HTTP_400_BAD_REQUEST)

class NotificationsView(APIView):
    def get(self, request, id):
        notifications = Notification.objects.filter(appointment=id)

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
        serialized_notifications = NotificationSerializer(data=notifications, many=True)
        return Response({"message": f"Notifications fetched successfully !", "data":serialized_notifications.data, "context":context}, status=status.HTTP_200_OK)

class CommunicationsView(APIView):
    def get(self, request):
        communications = Communication.objects.all()
        serialized_communications = CommunicationSerializer(communications, many=True)
        return Response({"message": f"Communications fetched successfully !", "data":serialized_communications.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        file = request.FILES["file"]
        title = request.data.get("title")
        communication_dic = {
            "title": title,
            "location": file
        }
        communication = CommunicationSerializer(data=communication_dic)
        if communication.is_valid():
            communication.save()
            return Response({"message": f"Communication added successfully !"}, status=status.HTTP_201_CREATED) 
        return Response({"message": communication.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        file = request.FILES["file"]
        title = request.data.get("title")
        communication_dic = {
            "title": title,
            "location": file
        }
        old_communication = Communication.objects.get(pk=id)
        communication = CommunicationSerializer(old_communication, data=communication_dic, partial=True)
        if communication.is_valid():
            communication.save()
            return Response({"message": f"Communication edited successfully !"}, status=status.HTTP_201_CREATED) 
        return Response({"message": communication.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        communication = Communication.objects.get(pk=id)
        communication.delete()
        return Response({"message": f"Communication deleted successfully !"}, status=status.HTTP_200_OK)


class PaymentView(APIView):
    def post(self, request):
        collect = campay.collect({
                "amount": "10",  # The amount you want to collect
                "currency": "XAF",
                # Phone number to request amount from. Must include country code
                "from": "237" + request.data.get("phone"),
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
            "user": request.data.get("user").id,
            "date": now(),
            'reference': collect.get('reference'),
            'external_reference': collect.get('external_reference'),
            # Phone number to request amount from. Must include country code
            "from": "237" + request.data.get("phone"),
            "description": "NATIONAL ID CARD FEES",
            "location": "Mendong"
            }
            userAppointment = Appointment.objects.get(user=request.data.get("user").id)
            print(f"User appointments: {userAppointment}")
            userAppointment.paid = True
            userAppointment.save()
            buffer = generate_pdf_file(payment_receipt_info)
            response = FileResponse(buffer, as_attachment=True, filename='mypdf.pdf', content_type='application/pdf')
            response.headers['Content-Disposition'] = 'inline; filename= "mypdf.pdf"'
            response.headers['Content-Type'] = 'application/pdf'
            return response
        else:
            userAppointment = Appointment.objects.get(user=request.data.get("user").id)
            userAppointment.paid = False
            userAppointment.save()
            if collect.get('reason'):
                context = {'message': collect.get('reason')}
            elif collect.get('message'):
                context = {'message': collect.get('message')}
            else:
                context = {
                    'message': 'An error occur with the payment please try later'}
            return Response({"message": context}, status=status.HTTP_400_BAD_REQUEST)
                
class DocumentView(APIView):
    def get(self,request):
        documents = Document.objects.all()
        serialized_documents = DocumentSerializer(documents, many=True)
        return Response({"message": f"Documents fetched successfully !", "data":serialized_documents.data}, status=status.HTTP_200_OK)
    
    def post(self,request):
        user_dic = {
            "user": request.data["user"],
            "birth_certificate": request.FILES["birth_certificate"],
            "proof_of_nationality": request.FILES["proof_of_nationality"],
            "passport_photos": request.FILES["passport_photos"],
            "residence_permit": request.FILES["residence_permit"],
            "marriage_certificate": request.FILES["marriage_certificate"],
            "death_certificate": request.FILES["death_certificate"],
            "sworn_statement": request.FILES["sworn_statement"]
        }
        document = DocumentSerializer(data=user_dic)
        if document.is_valid():
            document.save()
            return Response({"message":"Documents uploaded successfully!"}, status=status.HTTP_201_CREATED)
        return Response({"message": document.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request, document_id):
        document = Document.objects.get(pk=document_id)
        document.delete()
        return Response({"message": "Document deleted successfully !"}, status=status.HTTP_200_OK)

class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user:
            random_string = get_random_string(6)
            mail_subject = 'Reset your password'
            recepients = [f"{user.email}"]
            message = f"Enter the activation code to proceed: {random_string}"
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
                form = PasswordResetSerializer(data=data)
                if form.is_valid():
                    form.save()
            else:
                password_reset.code = random_string
                password_reset.save()
            return Response({"message": "We sent an activation code to your mail, check it", "data":UserSerializer(user).data}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid email"}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request):
        user = None
        try:
            user = User.objects.get(email=request.data["email"])
        except Exception as e:
            pass
        if user is None:
            return Response({"message": "Invalid email"}, status=status.HTTP_404_NOT_FOUND)
        password_reset = None
        try:
            password_reset = PasswordReset.objects.get(code=request.data["code"], user=user.pk)
        except Exception as e:
            pass
        if password_reset is None:
            return Response({"message": "Invalid activation code"}, status=status.HTTP_400_BAD_REQUEST)
        data_without_email = {
            "code": request.data["code"],
            "user": user.pk
        }
        reset_serializer = PasswordResetSerializer(data=data_without_email)
        if reset_serializer.is_valid():
            hashedPassword = make_password(request.data["new_password"])
            user.password = hashedPassword
            user.save()
            return Response({"message": "Password reset successful !"}, status=status.HTTP_200_OK)
        return Response({"message": reset_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)