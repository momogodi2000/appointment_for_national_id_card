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
        fields = ['id','username', 'email', 'password', 'groups', 'phone', 'profile_picture', 'role']

    def create(self, validated_data):
        groups_data = validated_data.pop('groups', None)  # Extract groups if present
        password = validated_data.pop('password')  # Extract the password to hash it

        user = User(**validated_data)  # Create user instance without saving it
        user.set_password(password)  # Hash the password
        user.save()  # Now save the user

        # If groups were provided, set them for the user
        if groups_data is not None:
            user.groups.set(groups_data)

        return user



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
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['date'] = str(instance.date)  # Ensure it's a string
        representation['time'] = str(instance.time)  # Ensure it's a string
        return representation





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
        return new_password_reset


class StatisticsSerializer(serializers.Serializer):
    user_count = serializers.IntegerField()
    appointment_count = serializers.IntegerField()
    document_count = serializers.IntegerField()
    missing_id_card_count = serializers.IntegerField()
    notification_count = serializers.IntegerField()
    communication_count = serializers.IntegerField()
    contact_us_count = serializers.IntegerField()
    password_reset_count = serializers.IntegerField()