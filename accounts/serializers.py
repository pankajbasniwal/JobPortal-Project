
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db import transaction

from .models import (
    UserProfile,
    StudentProfile,
    Company
)


class RegisterSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    role = serializers.ChoiceField(
        choices=['student', 'recruiter']
    )

    phone = serializers.CharField(required=False)
    education = serializers.CharField(required=False)
    skills = serializers.CharField(required=False)

    company_name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    website = serializers.URLField(
        required=False,
        allow_blank=True
    )
    location = serializers.CharField(required=False)

    def validate(self, data):

        if User.objects.filter(
            username=data['username']
        ).exists():
            raise serializers.ValidationError(
                "Username already exists"
            )

        if User.objects.filter(
            email__iexact=data['email']
        ).exists():
            raise serializers.ValidationError(
                "Email already exists"
            )

        validate_password(data['password'])

        if data['role'] == 'student':

            required_fields = ['phone', 'education', 'skills']

        else:

            required_fields = [
                'company_name', 'description', 'location'
            ]

        for field in required_fields:
            if not data.get(field):
                raise serializers.ValidationError(
                    {field: "This field is required"}
                )

        return data

    @transaction.atomic
    def create(self, validated_data):

        password = validated_data.pop('password')
        role = validated_data.pop('role')

        phone = validated_data.pop('phone', '')
        education = validated_data.pop('education', '')
        skills = validated_data.pop('skills', '')

        company_name = validated_data.pop(
            'company_name', ''
        )
        description = validated_data.pop(
            'description', ''
        )
        website = validated_data.pop('website', '')
        location = validated_data.pop('location', '')

        user = User.objects.create_user(
            password=password,
            **validated_data
        )

        UserProfile.objects.create(
            user=user,
            role=role
        )

        if role == 'student':

            StudentProfile.objects.create(
                user=user,
                phone=phone,
                education=education,
                skills=skills
            )

        else:

            Company.objects.create(
                user=user,
                company_name=company_name,
                description=description,
                website=website,
                location=location
            )

        return user
