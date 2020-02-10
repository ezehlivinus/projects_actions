from os.path import basename
from django.urls import path, include
from django.conf.urls import url
from the_rest_api.views import (ProjectViewSet, ActionViewSet)
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

router.register(r'project', ProjectViewSet, basename='project')
router.register(r'action', ActionViewSet, basename='action')

urlpatterns = [
    url(r'', include(router.urls)),
]