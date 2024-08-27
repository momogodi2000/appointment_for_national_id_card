from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from .models import *
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
    def create(self, validate_data):
        validate_data["password"] = make_password(validate_data["password"])
        new_user = User.objects.create(**validate_data)
        new_user.save()
        return new_user

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

class MissingIDCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissingIDCard
        fields = "__all__"
    def create(self, validate_data):
        new_idcard = MissingIDCard.objects.create(**validate_data)
        new_idcard.save()
        return new_idcard

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