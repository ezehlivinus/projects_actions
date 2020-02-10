# from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_204_NO_CONTENT
)
from rest_framework.response import Response
from the_rest_api.models import Project, Action
from the_rest_api.serializers import UserSerializer, ProjectSerializer, ActionSerializer

class ProjectViewSet(viewsets.viewSet):
    '''
    Project ViewSet:
    API endpoint that allows project to be viewed or edited
    '''

class ActionViewSet(viewsets.viewSet):
    '''
    Action ViewSet:
    API endpoint that allows project to be viewed or edited
    '''

class UserViewSet(viewsets.ModelViewSet):
    queryet = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

