from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ClientModel, ClientVisitHistoryModel
from .serializers import ClientSerializer, ClientVisitHistorySerializer


class ClientView(APIView):
    serializer_class = ClientSerializer
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        request_body=serializer_class,
        operation_summary='Create a new client',
        operation_description='Create a new client with the provided details',
        responses={201: 'Client created', 400: 'Bad Request'}
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Get all clients',
        operation_description='Get all clients',
        responses={200: ClientSerializer(many=True)}
    )
    def get(self, request):
        try:
            clients = ClientModel.objects.all()
            serializer = ClientSerializer(clients, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ClientModel.DoesNotExist:
            return Response({'detail': 'No clients found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ClientDetailView(APIView):
    serializer_class = ClientSerializer

    @swagger_auto_schema(
        operation_summary='Get a client',
        operation_description='Get a client by ID',
        responses={200: ClientSerializer}
    )
    def get(self, request, pk):
        try:
            client = ClientModel.objects.get(pk=pk)
            serializer = ClientSerializer(client)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ClientModel.DoesNotExist:
            return Response({'detail': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Update a client',
        operation_description='Update a client by ID',
        responses={200: ClientSerializer}
    )
    def put(self, request, pk):
        try:
            client = ClientModel.objects.get(pk=pk)
            serializer = ClientSerializer(client, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ClientModel.DoesNotExist:
            return Response({'detail': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Delete a client',
        operation_description='Delete a client by ID',
        responses={204: 'Client deleted'}
    )
    def delete(self, request, pk):
        try:
            client = ClientModel.objects.get(pk=pk)
            client.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ClientModel.DoesNotExist:
            return Response({'detail': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ClientVisitHistoryView(APIView):
    serializer_class = ClientVisitHistorySerializer

    @swagger_auto_schema(
        request_body=serializer_class,
        operation_summary='Add a visit history',
        operation_description='Add a visit history for a client',
        responses={201: 'Visit history added', 400: 'Bad Request'}
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            visit_count = serializer.validated_data['client'].visit_count
            serializer.validated_data['client'].visit_count = visit_count + 1
            serializer.validated_data['client'].save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Get all visit histories',
        operation_description='Get all visit histories',
        responses={200: ClientVisitHistorySerializer(many=True)}
    )
    def get(self, request):
        try:
            visit_histories = ClientVisitHistoryModel.objects.all()
            serializer = ClientVisitHistorySerializer(visit_histories, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ClientVisitHistoryModel.DoesNotExist:
            return Response({'detail': 'No visit histories found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ClientVisitHistoryDetailView(APIView):
    serializer_class = ClientVisitHistorySerializer

    @swagger_auto_schema(
        operation_summary='Get a visit history',
        operation_description='Get a visit history by ID',
        responses={200: ClientVisitHistorySerializer}
    )
    def get(self, request, pk):
        try:
            visit_history = ClientVisitHistoryModel.objects.get(pk=pk)
            serializer = ClientVisitHistorySerializer(visit_history)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ClientVisitHistoryModel.DoesNotExist:
            return Response({'detail': 'Visit history not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Update a visit history',
        operation_description='Update a visit history by ID',
        responses={200: ClientVisitHistorySerializer}
    )
    def put(self, request, pk):
        try:
            visit_history = ClientVisitHistoryModel.objects.get(pk=pk)
            serializer = ClientVisitHistorySerializer(visit_history, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ClientVisitHistoryModel.DoesNotExist:
            return Response({'detail': 'Visit history not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary='Delete a visit history',
        operation_description='Delete a visit history by ID',
        responses={204: 'Visit history deleted'}
    )
    def delete(self, request, pk):
        try:
            visit_history = ClientVisitHistoryModel.objects.get(pk=pk)
            visit_history.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ClientVisitHistoryModel.DoesNotExist:
            return Response({'detail': 'Visit history not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)