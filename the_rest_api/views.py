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

class ProjectViewSet(viewsets.ViewSet):
    '''
    Project ViewSet:
    API endpoint that allows project to be viewed or edited
    '''
    serializer_class = ProjectSerializer

    # POST: api/projects
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(status=HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(data=serializer.data, status=HTTP_201_CREATED)


    # GET: api/projects/<projectid>
    def retrieve(self, request, pk):
        try:
            project = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)

        serializer = ProjectSerializer(project)
        return Response(data=serializer.data, status=HTTP_200_OK)


    # GET: api/projects
    def list(self, request):
        queryset = Project.objects.all().order_by('-created_at')
        serializer = ProjectSerializer(queryset, many=True)
        return Response(data=serializer.data, status=HTTP_200_OK)

    # DELETE: api/projects/<projectid>
    def destroy(self, request, pk):
        try:
            project_detail = Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)
        project_detail.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    # PATCH: api/projects/<projectid>
    def partial_update(self, request, pk):
        project = Project.objects.filter(pk=pk).first()
        if not project:
            return Response(status=HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(project, data=request.data, partial=True)
        
        if serializer.is_valid():
            # fields to be updated: instance.field = new_value
            serializer.save()
            return Response(data=serializer.data, status=HTTP_200_OK)

    # PUT: api/projects/<projectid>
    def update(self, request, pk):
        project = Project.objects.filter(pk=pk).first()
        if not project:
            return Response(status=HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(data=serializer.data, status=HTTP_200_OK)

class ActionViewSet(viewsets.ViewSet):
    '''
    Action ViewSet:
    API endpoint that allows project to be viewed or edited
    '''
    pass

class UserViewSet(viewsets.ModelViewSet):
    queryet = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

