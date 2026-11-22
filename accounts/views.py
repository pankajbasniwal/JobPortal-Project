
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from .serializers import RegisterSerializer


# STUDENT AND RECRUITER REGISTRATION

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):

    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():

        user = serializer.save()

        return Response({
            "message": "Registration successful",
            "username": user.username,
            "role": user.userprofile.role
        }, status=status.HTTP_201_CREATED)

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


# USER LOGIN

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):

    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {"error": "Username and password required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(
        request,
        username=username,
        password=password
    )

    if user is not None:

        try:
            role = user.userprofile.role
        except Exception:
            return Response(
                {"error": "User role not configured"},
                status=status.HTTP_403_FORBIDDEN
            )

        token, created = Token.objects.get_or_create(
            user=user
        )

        return Response({
            "message": "Login successful",
            "token": token.key,
            "username": user.username,
            "role": role
        })

    return Response(
        {"error": "Invalid username or password"},
        status=status.HTTP_401_UNAUTHORIZED
    )
