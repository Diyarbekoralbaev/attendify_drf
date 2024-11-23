from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import EmployeeModel, EmployeeAttendanceModel
from .serializers import EmployeeSerializer, EmployeeAttendanceSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class EmployeeView(APIView):
    serializer_class = EmployeeSerializer
    # 
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        request_body=serializer_class,
        operation_summary='Create a new employee',
        operation_description='Create a new employee with the provided details',
        responses={201: 'Employee created', 400: 'Bad Request'}
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Get all employees',
        operation_description='Get all employees',
        responses={200: EmployeeSerializer(many=True)}
    )
    def get(self, request):
        try:
            employees = EmployeeModel.objects.all()
            serializer = EmployeeSerializer(employees, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except EmployeeModel.DoesNotExist:
            return Response({'detail': 'No employees found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDetailView(APIView):
    serializer_class = EmployeeSerializer
    

    @swagger_auto_schema(
        operation_summary='Get an employee',
        operation_description='Get an employee by ID',
        responses={200: EmployeeSerializer}
    )
    def get(self, request, pk):
        try:
            employee = EmployeeModel.objects.get(pk=pk)
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except EmployeeModel.DoesNotExist:
            return Response({'detail': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Update an employee',
        operation_description='Update an employee by ID',
        responses={200: EmployeeSerializer}
    )
    def put(self, request, pk):
        try:
            employee = EmployeeModel.objects.get(pk=pk)
            serializer = EmployeeSerializer(employee, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except EmployeeModel.DoesNotExist:
            return Response({'detail': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Delete an employee',
        operation_description='Delete an employee by ID',
        responses={204: 'Employee deleted'}
    )
    def delete(self, request, pk):
        try:
            employee = EmployeeModel.objects.get(pk=pk)
            employee.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except EmployeeModel.DoesNotExist:
            return Response({'detail': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EmployeeAttendanceView(APIView):
    serializer_class = EmployeeAttendanceSerializer
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        request_body=serializer_class,
        operation_summary='Create a new attendance',
        operation_description='Create a new attendance with the provided details',
        responses={201: 'Attendance created', 400: 'Bad Request'}
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Get all attendances',
        operation_description='Get all attendances',
        responses={200: EmployeeAttendanceSerializer(many=True)}
    )
    def get(self, request):
        try:
            attendances = EmployeeAttendanceModel.objects.all()
            serializer = EmployeeAttendanceSerializer(attendances, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except EmployeeAttendanceModel.DoesNotExist:
            return Response({'detail': 'No attendances found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EmployeeAttendanceDetailView(APIView):
    serializer_class = EmployeeAttendanceSerializer

    @swagger_auto_schema(
        operation_summary='Get an attendance',
        operation_description='Get an attendance by ID',
        responses={200: EmployeeAttendanceSerializer}
    )
    def get(self, request, pk):
        try:
            attendance = EmployeeAttendanceModel.objects.get(pk=pk)
            serializer = EmployeeAttendanceSerializer(attendance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except EmployeeAttendanceModel.DoesNotExist:
            return Response({'detail': 'Attendance not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Update an attendance',
        operation_description='Update an attendance by ID',
        responses={200: EmployeeAttendanceSerializer}
    )
    def put(self, request, pk):
        try:
            attendance = EmployeeAttendanceModel.objects.get(pk=pk)
            serializer = EmployeeAttendanceSerializer(attendance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except EmployeeAttendanceModel.DoesNotExist:
            return Response({'detail': 'Attendance not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Delete an attendance',
        operation_description='Delete an attendance by ID',
        responses={204: 'Attendance deleted'}
    )
    def delete(self, request, pk):
        try:
            attendance = EmployeeAttendanceModel.objects.get(pk=pk)
            attendance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except EmployeeAttendanceModel.DoesNotExist:
            return Response({'detail': 'Attendance not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
