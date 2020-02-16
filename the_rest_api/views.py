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
from rest_framework.decorators import api_view, action



class ProjectViewSet(viewsets.ViewSet):
    '''
    Project ViewSet:
    API endpoint that allows project to be viewed or edited
    '''

    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except:
            raise

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

# The paths below are for the endpoints that include actions and projects:
# api/projects/<project_id>/actions

    @action(methods=['post', 'get'], detail=True, url_path='actions')
    def actions(self, request, pk):
        # POST: api/projects/<projectid>/actions
        # create action(s) under this project
        if request.method == 'POST':
            project = self.get_object(pk)
            return ActionViewSet.create(ActionViewSet, request.data, pk)
        
        # POST: api/projects/<projectid>/actions
        # Retrieve all action that belong to a particular project
        if request.method == 'GET':
            project = self.get_object(pk)
            return ActionViewSet.project_actions(ActionViewSet, request.data, project)

    @action(methods=['get'], detail=True)
    def project_action(self, request, *args, **kwargs):
        #GET: 'projects/<int:pk>/actions/<int:action_id>/'
        # Retrieve a single action that belong to a particular project
        project = self.get_object(int(kwargs['project_id']))
        return ActionViewSet.project_action(ActionViewSet, project, int(kwargs['action_id']))

    @action(methods=['put'], detail=True)
    def project_action_update(self, request, *args, **kwargs):
        project = self.get_object(int(kwargs['project_id']))
        return ActionViewSet.project_action_update(ActionViewSet, request.data, project, int(kwargs['action_id']))

    @action(methods=['delete'], detail=True)
    def project_action_destroy(self, request, *args, **kwargs):
        try:
            project = self.get_object(int(kwargs['project_id']))
            return ActionViewSet.action_destroy(ActionViewSet, project.id, int(kwargs['action_id']))
        except:
            raise

        
        
class ActionViewSet(viewsets.ViewSet):
    '''
    Action ViewSet:
    API endpoint that allows action to be viewed or edited
    '''

    def get_object(self, pk):
        try:
            return Action.objects.get(pk=pk)
        except:
            raise

    serializer_class = ActionSerializer
    
    # POST: api/perojects/<projectid>/actions
    def create(self, request, pk):
        if request.method == 'GET':
            return Response(data={'error': 'check your routes'}, status=HTTP_400_BAD_REQUEST)

        data = { **request, 'project': pk,}

        serializer = self.serializer_class(data=data)

        if not serializer.is_valid():
            return Response(data={'error': 'Something went wrong: the data sent might not be valid'}, status=HTTP_400_BAD_REQUEST)
        serializer.save()

        return Response(data=serializer.data, status=HTTP_201_CREATED)
    

    # GET: api/actions
    def list(self, request):
        '''List all actions'''
        queryset = Action.objects.all().order_by('created_at')
        serializer = ActionSerializer(queryset, many=True)
        return Response(data=serializer.data, status=HTTP_200_OK)

    
        # GET: api/actions/<actionid>/
    def retrieve(self, request, pk):
        '''Retrieve a single action'''
        action = self.get_object(pk)
        serializer = ActionSerializer(action)
        return Response(data=serializer.data, status=HTTP_200_OK)

    def project_actions(self, request, project):
        '''
        GET: api/projects/<projectid>/actions
        retreive all actions that belong to particular a project
        Used at ProjectViewSet.actions
        '''
        try:
            actions = Action.objects.filter(project_id=project.id).order_by('-created_at')
            serializer = ActionSerializer(actions, many=True)
            return Response(data=serializer.data, status=HTTP_200_OK)
        except:
            raise
    
    def project_action(self, project, action_id):
        '''
        GET: api/projects/<projectid>/actions/actionid
        Retreive a actions that belong to particular a project
        Used at ProjectViewSet.project_action
        '''
        try:
            action = Action.objects.filter(pk=action_id, project_id=project.id)
            serializer = ActionSerializer(action, many=True)
            return Response(data=serializer.data, status=HTTP_200_OK )
        except:
            raise
    
    def project_action_update(self, request, project, action_id):
        try:
            action = Action.objects.filter(pk=action_id, project=project.id).first()

            data = {
                **request, 'project': project.id
            }
            
            serializer = self.serializer_class(action, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=HTTP_200_OK)
        except:
            raise
    
    def action_destroy(self, project_id, action_id):
        try:
            action = Action.objects.get(pk=action_id, project=project_id)
            action.delete()
            return Response(data={'message': 'action deleted'}, status=HTTP_204_NO_CONTENT)
        except:
            raise



class UserViewSet(viewsets.ModelViewSet):
    queryet = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

