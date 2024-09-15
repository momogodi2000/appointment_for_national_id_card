from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from .models import *
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


# clients 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return User.objects.create(**validated_data)
    
    

class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = "__all__"
    def create(self, validate_data):
        new_office = Office.objects.create(**validate_data)
        new_office.save()
        return new_office



class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"
    def create(self, validate_data):
        new_appointment = Appointment.objects.create(**validate_data)
        new_appointment.save()
        return new_appointment






class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"
    def create(self, validate_data):
        new_document = Document.objects.create(**validate_data)
        new_document.save()
        return new_document





from datetime import datetime


class MissingIDCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissingIDCard
        fields = ['name', 'email', 'phone', 'date_found', 'id_card_image']  # Specify fields explicitly

    def create(self, validated_data):
        return MissingIDCard.objects.create(**validated_data)
    



class SupportSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=500) 
    


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
    def create(self, validated_data):
        new_notification = Notification.objects.create(**validated_data)
        return new_notification



class CommunicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Communication
        fields = "__all__"
    def create(self, validated_data):
        new_communication =  Communication.objects.create(**validated_data)
        new_communication.save()
        return new_communication



class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = "__all__"
    
    def create(self, validated_data):
        new_contact_us = ContactUs.objects.create(**validated_data)
        new_contact_us.save()
        return new_contact_us


  
    
class PasswordResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordReset
        fields = "__all__"
    
    def create(self, validated_data):
        new_password_reset = PasswordReset.objects.create(**validated_data)
        new_password_reset.save()
        return new_password_reset