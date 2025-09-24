"""
URL configuration for A_sys project.

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
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from account.api.views import PasswordResetConfirmView, UserLoginView, UserLogoutView, ChangePasswordView, PasswordResetView


urlpatterns = [
    path('admin/logout/', auth_views.LogoutView.as_view(next_page='/admin/login/?next=/admin/'), name='admin-logout'),
    
    path('admin/', admin.site.urls),
    path('', include('account.urls',)),
    path('superadmin/', include('superadmin.urls' , namespace='superadmin')),
    path('manager/', include('manager.urls' , namespace='manager')),
    path('staff/', include('staff.urls' , namespace='staff')),

    #APIS (registration, login, logout, password change, password reset)
    path('api/v1/auth/login', UserLoginView.as_view(), name='login_user'),
    path('api/v1/auth/logout', UserLogoutView.as_view(), name='logout_user'),
    path('api/v1/auth/change-password', ChangePasswordView.as_view(), name='change-password'),
    path("api/v1/auth/password-reset", PasswordResetView.as_view(), name="password-reset"),
    path("api/v1/auth/password-reset/confirm", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)