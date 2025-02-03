"""
URL configuration for SoftDesk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers

from users.views import UserViewSet
from projects.views import ProjectViewSet, IssueViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('projects', ProjectViewSet, basename='projects')

projects_router = routers.NestedSimpleRouter(router,
                                          r'projects',
                                          lookup='project')
projects_router.register(r'issues', IssueViewSet, basename='issues')

issues_router = routers.NestedSimpleRouter(projects_router, r'issues', lookup='issue')
issues_router.register(r'comments', CommentViewSet, basename='comments')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('', include(projects_router.urls)),
    path('', include(issues_router.urls)),
]
