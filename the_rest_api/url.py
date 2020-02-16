from os.path import basename
from django.urls import path, include
from django.conf.urls import url
from the_rest_api.views import (ProjectViewSet, ActionViewSet)
from rest_framework.routers import DefaultRouter


router = DefaultRouter(trailing_slash=False)

router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'actions', ActionViewSet, basename='actions')
# router.register(r'actions', ActionViewSet, basename='actions')

urlpatterns = [
    url(r'', include(router.urls)),
    path('projects/<int:project_id>/actions/<int:action_id>', ProjectViewSet.as_view(
        {
        'get': 'project_action',
        'put': 'project_action_update',
        'delete': 'project_action_destroy',
        }
        )),
    
]
