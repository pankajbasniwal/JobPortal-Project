from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Job
from .serializers import JobSerializer


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def job_list(request):

    if request.method == 'GET':

        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)

        return Response(serializer.data)

    if not request.user.is_authenticated:
        return Response(
            {"error": "Please login first"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'recruiter':
        return Response(
            {"error": "Only recruiters can post jobs"},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        company = request.user.company
    except Exception:
        return Response(
            {"error": "Company profile not found"},
            status=status.HTTP_403_FORBIDDEN
        )

    serializer = JobSerializer(data=request.data)

    if serializer.is_valid():

        serializer.save(company=company)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])
def job_detail(request, id):

    try:
        job = Job.objects.get(id=id)

    except Job.DoesNotExist:
        return Response(
            {"error": "Job not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    if request.method == 'GET':

        serializer = JobSerializer(job)
        return Response(serializer.data)

    if not request.user.is_authenticated:
        return Response(
            {"error": "Please login first"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'recruiter':
        return Response(
            {"error": "Only recruiters can manage jobs"},
            status=status.HTTP_403_FORBIDDEN
        )

    if job.company.user_id != request.user.id:
        return Response(
            {"error": "You cannot manage another company's job"},
            status=status.HTTP_403_FORBIDDEN
        )

    if request.method == 'PUT':

        serializer = JobSerializer(
            job,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(company=job.company)
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    if request.method == 'DELETE':

        job.delete()

        return Response(
            {"message": "Job deleted successfully"}
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_jobs(request):

    if not hasattr(request.user, 'userprofile'):
        return Response(
            {"error": "User profile not found"},
            status=status.HTTP_403_FORBIDDEN
        )

    if request.user.userprofile.role != 'recruiter':
        return Response(
            {"error": "Only recruiters can view their jobs"},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        company = request.user.company
    except Exception:
        return Response(
            {"error": "Company profile not found"},
            status=status.HTTP_403_FORBIDDEN
        )

    jobs = Job.objects.filter(company=company).order_by('-posted_date')
    serializer = JobSerializer(jobs, many=True)

    return Response(serializer.data)
from django.shortcuts import render

def my_jobs_page(request):
    return render(request, 'my_jobs.html')
