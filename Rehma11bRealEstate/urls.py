"""Rehma11bRealEstate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from eproperty.views import userAccountViews,adminAccountViews
from django.conf.urls.static import static
from Rehma11bRealEstate import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth import views as auth_views
from eproperty.views import manage_users, manage_roles, manage_features
from eproperty.views.manage_users import UserList, UserCreate, UserUpdate, UserDelete,AssignRole, UserEnable
from eproperty.views.manage_roles import RoleDelete

urlpatterns = [
    path('', include('eproperty.urls')),
    path('admin/', admin.site.urls),
    path('register/', userAccountViews.register, name='register'),
    path('profile/', userAccountViews.profile, name='profile'),
    path('dashboard/', adminAccountViews.DashboardView.as_view(), name='dashboard'),
    path('login/', adminAccountViews.AdminLoginView.as_view()),
    path('logout/', adminAccountViews.LogoutView.as_view()),

                  path('users/', UserList.as_view(extra_context={'title': 'Manage Users'}), name='users'),
                  path('users/new/', UserCreate.as_view(extra_context={'title': 'Create User'}), name='create-user'),

                  path('users/<int:pk>/', UserUpdate.as_view(extra_context={'title': 'Edit User'}), name='edit-user'),
                  path('users/<int:pk>/assign-roles/',
                       AssignRole.as_view(extra_context={'title': 'Assign Roles to User'}),
                       name='assign-role'),
                  path('users/<int:pk>/enable-user/', UserEnable.as_view(extra_context={'title': 'Enable User'}),
                       name='enable-user'),
                  path('users/<int:pk>/delete-user/', UserDelete.as_view(extra_context={'title': 'Delete User'}),
                       name='delete-user'),
                  # path('users/<int:pk>/delete-user/', UserDelete.as_view(extra_context={'title': 'Delete User'}), name='delete-user'),
                  # path('users/<int:pk>/delete-user/', UserDelete.as_view(extra_context={'title': 'Delete User'}), name='delete-user'),
                  path('roles/', manage_roles.all_roles, name='roles'),
                  path('roles/new/', manage_roles.role, name='create-role'),
                  path('roles/<int:pk>/permissions/',
                       manage_roles.ManagePermission.as_view(extra_context={'title': 'Assign Features to Role'}),
                       name='permissions'),
                  path('roles/<int:pk>/delete-role/', RoleDelete.as_view(extra_context={'title': 'Delete Role'}),
                       name='delete-role'),
                  path('features/', manage_features.all_features, name='features'),
                  path('features/new/', manage_features.feature, name='create-feature'),
                  path('features/<int:pk>/delete/',
                       manage_features.FeatureDelete.as_view(extra_context={'title': 'Delete Feature'}),
                       name='delete-feature'),

                  path('login/', auth_views.LoginView.as_view(template_name='userAccountTemplates/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='userAccountTemplates/logout.html'), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
