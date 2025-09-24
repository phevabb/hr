from datetime import date, timedelta
from urllib.parse import unquote

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from account.models import (
    User, Department, Classes, Region, Districts,
    ManagementUnit, CurrentGrade, ChangeOfGrade, UserRemovalLog
)
from superadmin.api import ses as api_ses

User = get_user_model()

def get_birth_date_range(min_age, max_age):
    """Calculate birth date range for a given age range."""
    today = date.today()
    max_date = today - timedelta(days=min_age * 365.25)
    min_date = today - timedelta(days=(max_age + 1) * 365.25)
    return min_date, max_date

def get_stat_data(request, model_field, choices=None, related_field=None, output_key=None):
    """
    Generic function to generate statistics for a given model field or choices.
    
    Args:
        request: HTTP request object.
        model_field: Model field name or related field to count.
        choices: List of choices for fields with predefined choices (optional).
        related_field: Name of the related field for ForeignKey (optional).
        output_key: Key name for the output dictionary (e.g., 'department', 'region').
    
    Returns:
        Paginated Response with stat data.
    """
    users = User.objects.filter(is_active=True)
    if related_field:
        users = users.select_related(related_field).filter(**{f"{related_field}__isnull": False})
        counts = {obj[output_key]: 0 for obj in model_field.objects.values(output_key)}
        for user in users:
            related_obj = getattr(user, related_field, None)
            if related_obj:
                field_value = getattr(related_obj, output_key)
                counts[field_value] = counts.get(field_value, 0) + 1
    else:
        counts = {choice[0]: 0 for choice in choices}
        for user in users:
            if getattr(user, model_field, None):
                counts[getattr(user, model_field)] = counts.get(getattr(user, model_field), 0) + 1

    data = [{output_key: key, "count": count} for key, count in counts.items()]
    paginator = PageNumberPagination()
    result_page = paginator.paginate_queryset(data, request)
    return paginator.get_paginated_response(result_page)

@api_view(['GET'])
def department_stats(request):
    """Return count of active users per department."""
    users = User.objects.filter(is_active=True)
    
    # Initialize counts for all departments
    counts = {dept.department_name: 0 for dept in Department.objects.all()}
    
    for user in users:
        dept = getattr(user, 'directorate', None)
        if dept:
            counts[dept.department_name] += 1

    data = [{"department": k, "count": v} for k, v in counts.items()]
    paginator = PageNumberPagination()
    result_page = paginator.paginate_queryset(data, request)
    return paginator.get_paginated_response(result_page)

@api_view(['GET'])
def class_stats(request):
    """Return count of active users per class."""
    users = User.objects.filter(is_active=True)
    
    # Initialize counts for all classes
    counts = {cls.classes_name: 0 for cls in Classes.objects.all()}
    
    for user in users:
        cls = getattr(user, 'category', None)
        if cls:
            counts[cls.classes_name] += 1

    data = [{"class": k, "count": v} for k, v in counts.items()]
    paginator = PageNumberPagination()
    result_page = paginator.paginate_queryset(data, request)
    return paginator.get_paginated_response(result_page)

@api_view(['GET'])
def region_stats(request):
    """Return count of active users per region."""
    return get_stat_data(request, Region, related_field='region', output_key='region')

@api_view(['GET'])
def management_stats(request):
    users = User.objects.filter(is_active=True)
    counts = {mu.management_unit_name: 0 for mu in ManagementUnit.objects.all()}

    for user in users:
        mu = getattr(user, 'management_unit_cost_centre', None)
        if mu:
            counts[mu.management_unit_name] += 1

    data = [{"management_unit": k, "count": v} for k, v in counts.items()]
    paginator = PageNumberPagination()
    result_page = paginator.paginate_queryset(data, request)
    return paginator.get_paginated_response(result_page)

@api_view(['GET'])
def gender_stats(request):
    """Return count of active users per gender."""
    return get_stat_data(request, 'gender', choices=User.GENDER_CHOICES, output_key='gender')

@api_view(['GET'])
def leave_type_stats(request):
    """Return count of active users per leave type."""
    return get_stat_data(request, 'on_leave_type', choices=User.ON_LEAVE_TYPE_CHOICES, output_key='leave_type')

@api_view(['GET'])
def contract_stats(request):
    """Return count of active users per contract type."""
    return get_stat_data(request, 'fulltime_contract_staff', choices=User.CONTRACT_FULLTIME, output_key='contract_type')

@api_view(['GET'])
def senior_stats(request):
    """Return count of active users per staff category."""
    return get_stat_data(request, 'staff_category', choices=User.STAFF_CHOICES, output_key='staff_category')

@api_view(['GET'])
def pro_stats(request):
    """Return count of active users per professional type."""
    return get_stat_data(request, 'professional', choices=User.PROFESSIONAL_CHOICES, output_key='professional')

@api_view(['GET'])
def age_stats(request):
    """Return count of active users per age range."""
    age_ranges = {'20 - 30': (20, 30), '31 - 40': (31, 40), '41 - 50': (41, 50), '51 - 60': (51, 60), '61+': (61, 100)}
    counts = {key: 0 for key in age_ranges}
    
    for user in User.objects.filter(is_active=True, date_of_birth__isnull=False):
        age = user.age
        if age is not None:
            for range_label, (min_age, max_age) in age_ranges.items():
                if min_age <= age <= max_age:
                    counts[range_label] += 1

    data = [{"age_range": ar, "count": count} for ar, count in counts.items()]
    paginator = PageNumberPagination()
    result_page = paginator.paginate_queryset(data, request)
    return paginator.get_paginated_response(result_page)

@api_view(['GET'])
def grade_level_stats(request):
    """Return count of active users per salary level."""
    salary_levels = {f"SS.{i}": 0 for i in range(5, 26)}
    
    for user in User.objects.filter(is_active=True, current_salary_level__isnull=False):
        if user.current_salary_level in salary_levels:
            salary_levels[user.current_salary_level] += 1

    data = [{"salary_range": sr, "count": count} for sr, count in salary_levels.items()]
    paginator = PageNumberPagination()
    result_page = paginator.paginate_queryset(data, request)
    return paginator.get_paginated_response(result_page)

@api_view(['GET'])
def admin_dashboard_summary(request):
    """Return summary stats for admin dashboard."""
    stats = User.objects.filter(is_active=True).aggregate(
        num_of_users=Count('id'),
        num_of_females=Count('id', filter=Q(gender="Female")),
        num_of_males=Count('id', filter=Q(gender="Male")),
        num_of_staffs=Count('id', filter=Q(role="Staff")),
        num_of_admins=Count('id', filter=Q(role="Admin")),
        num_of_managers=Count('id', filter=Q(role="Manager")),
    )
    return Response(stats, status=status.HTTP_200_OK)

@api_view(['GET'])
def all_users(request):
    """Return paginated list of all active users."""
    users = User.objects.filter(is_active=True).order_by('first_name', 'last_name')
    paginator = PageNumberPagination()
    result_page = paginator.paginate_queryset(users, request)
    serializer = api_ses.UserSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
def all_users_to_excel(request):
    """Return all active users for Excel export."""
    users = User.objects.filter(is_active=True).order_by('first_name', 'last_name')
    serializer = api_ses.UserSerializerToExcel(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

class UserCreateAPIView(generics.CreateAPIView):
    """Create a new user."""
    queryset = User.objects.filter(is_active=True)
    serializer_class = api_ses.UserCreateSerializer
    permission_classes = [IsAuthenticated]

class UserDetailAPIView(generics.RetrieveAPIView):
    """Retrieve user details by ID."""
    queryset = User.objects.all()
    serializer_class = api_ses.UserSerializer
    lookup_field = 'pk'

class UserUpdateAPIView(generics.RetrieveUpdateAPIView):
    """Retrieve and update user details by ID."""
    queryset = User.objects.all()
    serializer_class = api_ses.UserUpdateSerializer
    lookup_field = 'pk'
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def update(self, request, *args, **kwargs):

       

        # Optionally, capture specific fields
        region_input = request.data.get("region")
     

        # Call the original update method to handle saving
        return super().update(request, *args, **kwargs)

class RegionList(generics.ListAPIView):
    """List all regions."""
    queryset = Region.objects.all()
    serializer_class = api_ses.RegionSerializer

class DistrictList(generics.ListAPIView):
    """List all districts."""
    queryset = Districts.objects.all()
    serializer_class = api_ses.DistrictSerializer

class DepartmentList(generics.ListAPIView):
    """List all departments."""
    queryset = Department.objects.all()
    serializer_class = api_ses.DepartmentSerializer

class ClassesList(generics.ListAPIView):
    """List all classes."""
    queryset = Classes.objects.all()
    serializer_class = api_ses.ClassesSerializer

class ManagementUnitList(generics.ListAPIView):
    """List all management units."""
    queryset = ManagementUnit.objects.all()
    serializer_class = api_ses.ManagementUnitSerializer

class CurrentGradeList(generics.ListAPIView):
    """List all current grades."""
    queryset = CurrentGrade.objects.all()
    serializer_class = api_ses.CurrentGradeSerializer

class ChangeOfGradeList(generics.ListAPIView):
    """List all change of grades."""
    queryset = ChangeOfGrade.objects.all()
    serializer_class = api_ses.ChangeOfGradeSerializer

class UserFieldsAPIView(APIView):
    """Return metadata for User model fields."""
    def get(self, request):
        fields = []
        ignored_fields = {
            "id", "password", "last_login", "is_superuser", "is_staff",
            "is_active", "date_joined", "groups", "user_permissions"
        }
        
        for field in User._meta.get_fields():
            if field.auto_created and not field.concrete:
                continue
            if field.name in ignored_fields:
                continue

            field_info = {
                "field_name": field.name,
                "field_type": field.get_internal_type(),
                "multiple": field.get_internal_type() == "ManyToManyField"
            }

            if getattr(field, "choices", None):
                field_info["choices"] = list(field.choices)

            if field.get_internal_type() in ["ForeignKey", "ManyToManyField"]:
                related_model = field.related_model
                field_info["items"] = [
                    {"id": obj.id, "name": str(obj)} for obj in related_model.objects.all()
                ]

            fields.append(field_info)
        return Response(fields, status=status.HTTP_200_OK)

@api_view(['POST'])
def remove_user(request):
    """Remove a user by setting is_active to False and log the reason."""
    user_id = request.data.get('user_id')
    reason = request.data.get('reason')

    if not user_id or not reason:
        return Response({"error": "user_id and reason are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(id=user_id)
        user.is_active = False
        user.save()

        UserRemovalLog.objects.create(
            user=user,
            reason=reason,
            removed_at=timezone.now()
        )
        return Response({"message": "User removed successfully"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
def users_per_department(request):
    """Return paginated list of users filtered by department or other criteria."""
    dept = unquote(request.GET.get("dept", "")).strip()
    users = User.objects.none()
    filter_key = None

    try:
        reference_lists = {
            "department": Department.objects.values_list("department_name", flat=True),
            "class": Classes.objects.values_list("classes_name", flat=True),
            "region": Region.objects.values_list("region", flat=True),
            "unit": ManagementUnit.objects.values_list("management_unit_name", flat=True),
            "staff category": [choice[0] for choice in User.STAFF_CHOICES],
            "gender category": [choice[0] for choice in User.GENDER_CHOICES],
            "leave type": [choice[0] for choice in User.ON_LEAVE_TYPE_CHOICES],
            "agreement type": [choice[0] for choice in User.CONTRACT_FULLTIME],
            "professional type": ["Professional", "Subprofessional"],
            "salary range": {f"SS.{i}": f"SS.{i}" for i in range(5, 26)},
            "age range": {
                "20 - 30": (20, 30), "31 - 40": (31, 40), "41 - 50": (41, 50),
                "51 - 60": (51, 60), "61+": (61, 100)
            }
        }

        for key, values in reference_lists.items():
            if dept in values:
                filter_key = key
                if key == "department":
                    users = User.objects.filter(directorate__department_name__iexact=dept, is_active=True)
                elif key == "class":
                    users = User.objects.filter(category__classes_name__iexact=dept, is_active=True, category__isnull=False)
                elif key == "region":
                    users = User.objects.filter(region__region__iexact=dept, is_active=True)
                elif key == "unit":
                    users = User.objects.filter(management_unit_cost_centre__management_unit_name__iexact=dept, is_active=True, management_unit_cost_centre__isnull=False)
                elif key == "staff category":
                    users = User.objects.filter(staff_category=dept, is_active=True)
                elif key == "gender category":
                    users = User.objects.filter(gender=dept, is_active=True)
                elif key == "leave type":
                    users = User.objects.filter(on_leave_type=dept, is_active=True)
                elif key == "agreement type":
                    users = User.objects.filter(fulltime_contract_staff=dept, is_active=True)
                elif key == "professional type":
                    users = User.objects.filter(professional=dept, is_active=True)
                elif key == "salary range":
                    users = User.objects.filter(current_salary_level=dept, is_active=True)
                elif key == "age range":
                    min_age, max_age = values[dept]
                    min_date, max_date = get_birth_date_range(min_age, max_age)
                    users = User.objects.filter(
                        date_of_birth__gte=min_date,
                        date_of_birth__lte=max_date,
                        date_of_birth__isnull=False,
                        is_active=True
                    )
                break

        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(users, request)
        serializer = api_ses.UserSerializer(result_page, many=True)
        filtered_users = [
            {k: v for k, v in user.items() if k not in ["staff_category", "districts"]}
            for user in serializer.data
        ]

        return paginator.get_paginated_response({
            "dept": dept,
            "filter_type": filter_key,
            "count": users.count(),
            "users": filtered_users,
        })
    except Exception as e:
        return Response({
            "dept": dept,
            "filter_type": None,
            "count": 0,
            "users": [],
            "error": str(e),
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
def users_per_department_no_pages(request):
    """Return non-paginated list of users filtered by department or other criteria."""
    dept = unquote(request.GET.get("dept", "")).strip()
    users = User.objects.none()
    filter_key = None

    try:
        reference_lists = {
            "department": Department.objects.values_list("department_name", flat=True),
            "class": Classes.objects.values_list("classes_name", flat=True),
            "region": Region.objects.values_list("region", flat=True),
            "unit": ManagementUnit.objects.values_list("management_unit_name", flat=True),
            "staff category": [choice[0] for choice in User.STAFF_CHOICES],
            "gender category": [choice[0] for choice in User.GENDER_CHOICES],
            "leave type": [choice[0] for choice in User.ON_LEAVE_TYPE_CHOICES],
            "agreement type": [choice[0] for choice in User.CONTRACT_FULLTIME],
            "professional type": ["Professional", "Subprofessional"],
            "salary range": {f"SS.{i}": f"SS.{i}" for i in range(5, 26)},
            "age range": {
                "20 - 30": (20, 30), "31 - 40": (31, 40), "41 - 50": (41, 50),
                "51 - 60": (51, 60), "61+": (61, 100)
            }
        }

        for key, values in reference_lists.items():
            if dept in values:
                filter_key = key
                if key == "department":
                    users = User.objects.filter(directorate__department_name__iexact=dept, is_active=True)
                elif key == "class":
                    users = User.objects.filter(category__classes_name__iexact=dept, is_active=True, category__isnull=False)
                elif key == "region":
                    users = User.objects.filter(region__region__iexact=dept, is_active=True)
                elif key == "unit":
                    users = User.objects.filter(management_unit_cost_centre__management_unit_name__iexact=dept, is_active=True, management_unit_cost_centre__isnull=False)
                elif key == "staff category":
                    users = User.objects.filter(staff_category=dept, is_active=True)
                elif key == "gender category":
                    users = User.objects.filter(gender=dept, is_active=True)
                elif key == "leave type":
                    users = User.objects.filter(on_leave_type=dept, is_active=True)
                elif key == "agreement type":
                    users = User.objects.filter(fulltime_contract_staff=dept, is_active=True)
                elif key == "professional type":
                    users = User.objects.filter(professional=dept, is_active=True)
                elif key == "salary range":
                    users = User.objects.filter(current_salary_level=dept, is_active=True)
                elif key == "age range":
                    min_age, max_age = values[dept]
                    min_date, max_date = get_birth_date_range(min_age, max_age)
                    users = User.objects.filter(
                        date_of_birth__gte=min_date,
                        date_of_birth__lte=max_date,
                        date_of_birth__isnull=False,
                        is_active=True
                    )
                break

        serializer = api_ses.UserSerializer(users, many=True)
        filtered_users = [
            {k: v for k, v in user.items() if k not in ["staff_category", "districts"]}
            for user in serializer.data
        ]

        return Response({
            "dept": dept,
            "filter_type": filter_key,
            "count": users.count(),
            "users": filtered_users,
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            "dept": dept,
            "filter_type": None,
            "count": 0,
            "users": [],
            "error": str(e),
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)