from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, LoginSerializer, ResetPasswordSerializer
from .models import UserModel
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class RegisterView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    @swagger_auto_schema(
        tags=['Users'],
        operation_id='Register a new user',
        operation_summary='Register a new user',
        operation_description='Register a new user with the provided details',
        request_body=UserSerializer,
        responses={
            201: UserSerializer(),
        }
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=['Users'],
        operation_id='Get all users',
        operation_summary='Get all users',
        operation_description='Get all users',
        responses={
            200: UserSerializer(many=True),
        }
    )
    def get(self, request):
        users = UserModel.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=['Users'],
        operation_id='Login',
        operation_summary='Login',
        operation_description='Login with the provided username and password',
        request_body=LoginSerializer,
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                'access': openapi.Schema(type=openapi.TYPE_STRING),
            }
        )}
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Users'],
        operation_id='Get current user',
        operation_summary='Get current user',
        operation_description='Get the currently authenticated user',
        responses={200: UserSerializer()}
    )
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Users'],
        operation_id='Get user details',
        operation_summary='Get user details',
        operation_description='Get the details of a user by their ID',
        responses={200: UserSerializer()}
    )
    def get(self, request, user_id):
        user = UserModel.objects.get(id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=['Users'],
        operation_id='Update user details',
        operation_summary='Update user details',
        operation_description='Update the details of a user by their ID',
        request_body=UserSerializer,
        responses={200: UserSerializer()}
    )
    def put(self, request, user_id):
        user = UserModel.objects.get(id=user_id)
        if user.role == 'admin' or user == request.user:
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'You do not have permission to perform this action'},
                            status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=['Users'],
        operation_id='Delete user',
        operation_summary='Delete user',
        operation_description='Delete a user by their ID',
        responses={204: 'No Content'}
    )
    def delete(self, request, user_id):
        user = UserModel.objects.get(id=user_id)
        if user.role == 'admin':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'detail': 'You do not have permission to perform this action'},
                            status=status.HTTP_403_FORBIDDEN)


class ResetPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Users'],
        operation_id='Reset password',
        operation_summary='Reset password',
        operation_description='Reset the password of the currently authenticated user',
        request_body=ResetPasswordSerializer,
        responses={200: UserSerializer()}
    )
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
