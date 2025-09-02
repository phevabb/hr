from django.urls import path
from . import  views
from .views import UserCreateView, UserUpdateView, UserDetailView
app_name = 'superadmin'
from superadmin.api import views as api_views




urlpatterns = [

    path('new_entry/', UserCreateView.as_view(), name='new_entry'),
    path("users/by-department/", views.users_by_department, name="users_by_department"),


    path('users/<int:pk>/edit/', UserUpdateView.as_view(), name='user_edit'),
    path('users/<int:pk>/detail/', UserDetailView.as_view(), name='user_detail'),
    path('home/', views.index,name='dashboard' ),
    path('ana_distribution/', views.distribution,name='ana_distribution' ),
    path('ana_movement/', views.movement,name='ana_movement' ),
    path('ana_training/', views.training,name='ana_training' ),
    path('all_users/', views.all_users,name='all_users' ),


    # API endpoint for statistics (admin dashboard)  
    path('api/v1/class-stats', api_views.class_stats, name='class_stats_api'),
    path('api/v1/directorate-stats', api_views.department_stats, name='department_stats_api'),
    path('api/v1/region-stats', api_views.region_stats, name='region_stats_api'),
    path('api/v1/management-stats', api_views.management_stats, name='management_stats_api'),
    path('api/v1/senior-stats', api_views.senior_stats, name='senior_stats_api'),
    path('api/v1/gender-stats', api_views.gender_stats, name='gender_stats_api'),
    path('api/v1/age-stats', api_views.age_stats, name='age_stats_api'),
    path('api/v1/salary-grade-stats', api_views.grade_level_stats, name='salary_grade_stats_api'),
    path('api/v1/leave-stats', api_views.leave_type_stats, name='leave_stats_api'),
    path('api/v1/contract-stats', api_views.contract_stats, name='contract_stats_api'),
    path('api/v1/pro-stats', api_views.pro_stats, name='pro_stats_api'),
        # admin_dashboard_summary (4 boxes)
    path('api/v1/admin-dashboard-summary', api_views.admin_dashboard_summary, name='admin_dashboard_summary_api'),
    path('api/v1/all-users', api_views.all_users, name='all_users_api'),
    path("api/v1/users/create", api_views.UserCreateAPIView.as_view(), name="user-create"),

    # dynamic api options
    path('api/v1/regions', api_views.RegionList.as_view(), name='regions-list'),
    path('api/v1/districts', api_views.DistrictList.as_view(), name='districts-list'),
    path('api/v1/departments', api_views.DepartmentList.as_view(), name='departments-list'),
    path('api/v1/classes', api_views.ClassesList.as_view(), name='classes-list'),
    path('api/v1/management-units', api_views.ManagementUnitList.as_view(), name='management-units-list'),
    path('api/v1/current-grades', api_views.CurrentGradeList.as_view(), name='current-grades-list'),
    path('api/v1/change-of-grades', api_views.ChangeOfGradeList.as_view(), name='change-of-grades-list'),

    # FOR FIELDS IN USER MODEL
    path('api/v1/user-fields', api_views.UserFieldsAPIView.as_view(), name='user-fields'),

    path("api/v1/users/<int:pk>/", api_views.UserDetailAPIView.as_view(), name="user-detail"),

]
