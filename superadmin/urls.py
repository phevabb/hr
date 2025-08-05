from django.urls import path
from . import  views
from .views import UserCreateView, UserUpdateView
app_name = 'superadmin'

urlpatterns = [
    path('new_entry/', UserCreateView.as_view(), name='new_entry'),
    path('users/<int:pk>/edit/', UserUpdateView.as_view(), name='user_edit'),
    path('', views.index,name='dashboard' ),
    path('all_users/', views.all_users,name='all_users' ),


]
