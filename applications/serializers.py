
from rest_framework import serializers
from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):

    student_name = serializers.CharField(
        source='student.username',
        read_only=True
    )

    job_title = serializers.CharField(
        source='job.title',
        read_only=True
    )

    company_name = serializers.CharField(
        source='job.company.company_name',
        read_only=True
    )

    class Meta:
        model = Application
        fields = [
            'id',
            'student',
            'student_name',
            'job',
            'job_title',
            'company_name',
            'resume',
            'status',
            'applied_date'
        ]

        read_only_fields = [
            'student',
            'status',
            'applied_date'
        ]

        extra_kwargs = {
    'resume': {'required': True}
}


class ApplicationStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        fields = ['status']
