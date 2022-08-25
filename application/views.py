from django.db import connection
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response

from application.pagination import BasicPagination
from application.serializers.client import ClientSerializer
from application.serializers.message import MessageSerializer
from application.serializers.notification import NotificationSerializer
from application.entities.client import Client
from application.entities.message import Message
from application.entities.notification import Notification


class ClientListAPIView(APIView, BasicPagination):
    """
    Get list of all clients or create new client
    """
    def get(self, request: Request, format=None) -> Response:
        """
        Get list of clients
        """
        clients = self.paginate_queryset(Client.objects.all(), request, view=self)
        client_serializer = ClientSerializer(clients, many=True)
        return Response(client_serializer.data)

    def post(self, request: Request, format=None) -> Response:
        """
        Create a new client or 400 (bad request)
        """
        client_serializer = ClientSerializer(data=request.data)
        if not client_serializer.is_valid():
            return Response(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        client_serializer.save()
        return Response('client was created successfully', status=status.HTTP_201_CREATED)


class ClientAPIView(APIView):
    """
    Get, update or delete a client instance
    """
    def get(self, request: Request, pk: int, format=None) -> Response:
        """
        Get client by id
        """
        client = get_object_or_404(Client, pk=pk)
        client_serializer = ClientSerializer(client)
        return Response(client_serializer.data)

    def put(self, request: Request, pk: int, format=None) -> Response:
        """
        Update client by id
        """
        client = get_object_or_404(Client, pk=pk)
        client_serializer = ClientSerializer(client, data=request.data, partial=True)
        if not client_serializer.is_valid():
            return Response(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        client_serializer.save()
        return Response('client was updated successfully', status=status.HTTP_200_OK)

    def delete(self, request: Request, pk: int, format=None) -> Response:
        """
        Delete client by id
        """
        client = get_object_or_404(Client, pk=pk)
        client.delete()
        return Response('client was deleted successfully', status=status.HTTP_204_NO_CONTENT)


class NotificationListAPIView(APIView, BasicPagination):
    """
    Get list of all notifications or create new notification
    """
    def get(self, request: Request, format=None) -> Response:
        """
        Get list of notifications
        """
        notifications = Notification.objects.all()
        query_params = request.GET
        tag = query_params.get('tag')
        mobile_operator_code = query_params.get('mobile_operator_code')
        if tag:
            notifications = notifications.filter(tag=tag)
        if mobile_operator_code:
            notifications = notifications.filter(mobile_operator_code=mobile_operator_code)
        notifications = self.paginate_queryset(notifications, request, view=self)
        notification_serializer = NotificationSerializer(notifications, many=True)
        return Response(notification_serializer.data)

    def post(self, request: Request, format=None) -> Response:
        """
        Create a new notification
        """
        notification_serializer = NotificationSerializer(data=request.data)
        if not notification_serializer.is_valid():
            return Response(notification_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        notification_serializer.save()
        return Response('notification was created successfully', status=status.HTTP_201_CREATED)


class NotificationAPIView(APIView, BasicPagination):
    def get(self, request: Request, pk: int, format=None) -> Response:
        """
        Get notification by id
        """
        notification = get_object_or_404(Notification, pk=pk)
        notification_serializer = NotificationSerializer(notification)
        return Response(notification_serializer.data)

    def put(self, request: Request, pk: int, format=None) -> Response:
        """
        Update notification by id
        """
        notification = get_object_or_404(Notification, pk=pk)
        notification_serializer = NotificationSerializer(notification, data=request.data, partial=True)
        if not notification_serializer.is_valid():
            return Response(notification_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        notification_serializer.save()
        return Response('notification was updated successfully', status=status.HTTP_200_OK)

    def delete(self, request: Request, pk: int, format=None) -> Response:
        """
        Delete notification by id
        """
        notification = get_object_or_404(Notification, pk=pk)
        notification.delete()
        return Response('notification was deleted successfully', status=status.HTTP_204_NO_CONTENT)


class MessageAPIView(APIView):
    pass
