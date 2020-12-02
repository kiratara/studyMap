from django.contrib.auth.models import User
from rest_framework import filters, status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from map import models, serializers


class TopicViewSet(viewsets.ModelViewSet):
    """Handle CRUD for Topic model"""
    serializer_class = serializers.TopicSerializer
    queryset = models.Topic.objects.all()
    filter_backends = (filters.SearchFilter, )
    search_fields = ('title', )


class SubTopicViewSet(viewsets.ModelViewSet):
    """Handle CRUD for SubTopic model"""
    serializer_class = serializers.SubTopicSerializers
    queryset = models.SubTopic.objects.all()


class NoteViewSet(viewsets.ModelViewSet):
    """Handle CRUD for Note Model"""
    serializer_class = serializers.NoteSerializer
    queryset = models.Note.objects.all()

