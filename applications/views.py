
from rest_framework.decorators import (
    api_view,
    permission_classes,
    parser_classes
)

from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework.response import Response
from rest_framework import status

from .models import Application
from .serializers import (
    ApplicationSerializer,
    ApplicationStatusSerializer
)

from jobs.models import Job


# STUDENT APPLY FOR JOB

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def apply_job(request, job_id):

    if not hasattr(request.user, 'userprofile'):
        return Response(
            {"error": "User profile not found"},
            status=status.HTTP_403_FORBIDDEN
        )

    if request.user.userprofile.role != 'student':
        return Response(
            {"error": "Only students can apply"},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        job = Job.objects.get(id=job_id)

    except Job.DoesNotExist:
        return Response(
            {"error": "Job not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if Application.objects.filter(
        student=request.user,
        job=job
    ).exists():

        return Response(
            {"error": "You already applied for this job"},
            status=status.HTTP_400_BAD_REQUEST
        )

    serializer = ApplicationSerializer(
        data={
            'job': job.id,
            'resume': request.FILES.get('resume')
        }
    )

    if serializer.is_valid():

        serializer.save(
            student=request.user,
            job=job
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


# STUDENT VIEW OWN APPLICATIONS

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_applications(request):

    if not hasattr(request.user, 'userprofile'):
        return Response(
            {"error": "User profile not found"},
            status=status.HTTP_403_FORBIDDEN
        )

    if request.user.userprofile.role != 'student':
        return Response(
            {"error": "Only students can view this page"},
            status=status.HTTP_403_FORBIDDEN
        )

    applications = Application.objects.filter(
        student=request.user
    )

    serializer = ApplicationSerializer(
        applications,
        many=True
    )

    return Response(serializer.data)


# RECRUITER VIEW APPLICANTS

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recruiter_applications(request):

    if not hasattr(request.user, 'userprofile'):
        return Response(
            {"error": "User profile not found"},
            status=status.HTTP_403_FORBIDDEN
        )

    if request.user.userprofile.role != 'recruiter':
        return Response(
            {"error": "Only recruiters can view applicants"},
            status=status.HTTP_403_FORBIDDEN
        )

    applications = Application.objects.filter(
        job__company__user=request.user
    )

    serializer = ApplicationSerializer(
        applications,
        many=True
    )

    return Response(serializer.data)


# RECRUITER UPDATE APPLICATION STATUS

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_application_status(request, id):

    if not hasattr(request.user, 'userprofile'):
        return Response(
            {"error": "User profile not found"},
            status=status.HTTP_403_FORBIDDEN
        )

    if request.user.userprofile.role != 'recruiter':
        return Response(
            {"error": "Only recruiters can update status"},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        application = Application.objects.get(
            id=id,
            job__company__user=request.user
        )

    except Application.DoesNotExist:
        return Response(
            {"error": "Application not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = ApplicationStatusSerializer(
        application,
        data=request.data
    )

    if serializer.is_valid():

        serializer.save()

        return Response({
            "message": "Application status updated",
            "status": serializer.data['status']
        })

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )
