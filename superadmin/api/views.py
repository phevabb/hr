from datetime import date

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from account.models import (
    User,
    Department,
    Classes,
    Region,
    Districts,
    ManagementUnit,
    CurrentGrade,
    ChangeOfGrade,
)

from superadmin.api import ses as api_ses
from .ses import UserCreateSerializer










User = get_user_model()
users = User.objects.all()


# Analysis of Staff Distribution API
# directorate stats
# directorate stats
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from account.models import User, Department

@api_view(['GET'])
def department_stats(request):
    user_queryset = User.objects.select_related('directorate').all()

    # Initialize all departments with 0
    all_departments = Department.objects.all()
    department_counts = {dept.department_name: 0 for dept in all_departments}

    # Count users in each department
    for user in user_queryset:
        if user.directorate:
            department_name = user.directorate.department_name
            department_counts[department_name] += 1

    # Table format
    department_data = [
        {"department": dept, "count": count}
        for dept, count in department_counts.items()
    ]

    # Use DRF default paginator from settings
    paginator = PageNumberPagination()
    result_page = paginator.paginate_queryset(department_data, request)

    return paginator.get_paginated_response(result_page)




from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from account.models import User, Department, Classes, Region, ManagementUnit

# Class stats
@api_view(['GET'])
def class_stats(request):
    users = User.objects.select_related('category').all()
    class_counts = {cls.classes_name: 0 for cls in Classes.objects.all()}

    for user in users:
        if user.category:
            class_counts[user.category.classes_name] += 1

    class_data = [{"class": cls, "count": count} for cls, count in class_counts.items()]

    paginator = PageNumberPagination()
    result_page = paginator.paginate_queryset(class_data, request)
    return paginator.get_paginated_response(result_page)


# Region stats
@api_view(['GET'])
def region_stats(request):
    users = User.objects.select_related('region').all()
    region_counts = {reg.region: 0 for reg in Region.objects.all()}

    for user in users:
        if user.region:
            region_counts[user.region.region] += 1

    region_data = [{"region": reg, "count": count} for reg, count in region_counts.items()]

    paginator = PageNumberPagination()
    result_page = paginator.paginate_queryset(region_data, request)
    return paginator.get_paginated_response(result_page)


# Management stats
@api_view(['GET'])
def management_stats(request):
    users = User.objects.select_related('management_unit_cost_centre').all()
    management_counts = {mu.management_unit_name: 0 for mu in ManagementUnit.objects.all()}

    for user in users:
        if user.management_unit_cost_centre:
            management_counts[user.management_unit_cost_centre.management_unit_name] += 1

    management_data = [{"management_unit": mu, "count": count} for mu, count in management_counts.items()]

    paginator = PageNumberPagination()
    result_page = paginator.paginate_queryset(management_data, request)
    return paginator.get_paginated_response(result_page)


# Gender stats
@api_view(['GET'])
def gender_stats(request):
    users = User.objects.all()
    gender_counts = {choice[0]: 0 for choice in User.GENDER_CHOICES}

    for user in users:
        if user.gender:
            gender_counts[user.gender] += 1

    gender_data = [{"gender": g, "count": c} for g, c in gender_counts.items()]

    paginator = PageNumberPagination()
    result_page = paginator.paginate_queryset(gender_data, request)
    return paginator.get_paginated_response(result_page)


# Age stats
@api_view(['GET'])
def age_stats(request):
    users = User.objects.all()
    age_ranges = {'20 - 30': 0, '31 - 40': 0, '41 - 50': 0, '51 - 60': 0, '61+': 0}

    for user in users:
        if user.age is not None:
            if 20 <= user.age <= 30:
                age_ranges['20 - 30'] += 1
            elif 31 <= user.age <= 40:
                age_ranges['31 - 40'] += 1
            elif 41 <= user.age <= 50:
                age_ranges['41 - 50'] += 1
            elif 51 <= user.age <= 60:
                age_ranges['51 - 60'] += 1
            elif user.age >= 61:
                age_ranges['61+'] += 1

    age_data = [{"age_range": ar, "count": count} for ar, count in age_ranges.items()]

    paginator = PageNumberPagination()
    result_page = paginator.paginate_queryset(age_data, request)
    return paginator.get_paginated_response(result_page)


# Grade level stats
@api_view(['GET'])
def grade_level_stats(request):
    users = User.objects.all()
    salary_levels = {f"SS.{i}": 0 for i in range(5, 26)}

    for user in users:
        if user.current_salary_level:
            salary_levels[user.current_salary_level] = salary_levels.get(user.current_salary_level, 0) + 1

    salary_data = [{"salary_range": sr, "count": count} for sr, count in salary_levels.items()]

    paginator = PageNumberPagination()
    result_page = paginator.paginate_queryset(salary_data, request)
    return paginator.get_paginated_response(result_page)


# Leave type stats
@api_view(['GET'])
def leave_type_stats(request):
    users = User.objects.all()
    leave_counts = {choice[0]: 0 for choice in User.ON_LEAVE_TYPE_CHOICES}

    for user in users:
        if user.on_leave_type:
            leave_counts[user.on_leave_type] += 1

    leave_data = [{"leave_type": lt, "count": count} for lt, count in leave_counts.items()]

    paginator = PageNumberPagination()
    result_page = paginator.paginate_queryset(leave_data, request)
    return paginator.get_paginated_response(result_page)


# Contract stats
@api_view(['GET'])
def contract_stats(request):
    users = User.objects.all()
    contract_counts = {choice[0]: 0 for choice in User.CONTRACT_FULLTIME}

    for user in users:
        if user.fulltime_contract_staff:
            contract_counts[user.fulltime_contract_staff] += 1

    contract_data = [{"contract_type": ct, "count": count} for ct, count in contract_counts.items()]

    paginator = PageNumberPagination()
    result_page = paginator.paginate_queryset(contract_data, request)
    return paginator.get_paginated_response(result_page)


# Senior/Junior staff stats
@api_view(['GET'])
def senior_stats(request):
    users = User.objects.all()
    staff_counts = {choice[0]: 0 for choice in User.STAFF_CHOICES}

    for user in users:
        if user.staff_category:
            staff_counts[user.staff_category] += 1

    staff_data = [{"staff_category": sc, "count": count} for sc, count in staff_counts.items()]

    paginator = PageNumberPagination()
    result_page = paginator.paginate_queryset(staff_data, request)
    return paginator.get_paginated_response(result_page)


# Professional stats
@api_view(['GET'])
def pro_stats(request):
    users = User.objects.all()
    professional_counts = {choice[0]: 0 for choice in User.PROFESSIONAL_CHOICES}

    for user in users:
        if user.professional:
            professional_counts[user.professional] += 1

    pro_data = [{"professional": p, "count": count} for p, count in professional_counts.items()]

    paginator = PageNumberPagination()
    result_page = paginator.paginate_queryset(pro_data, request)
    return paginator.get_paginated_response(result_page)





# 4 boxex on admin dashboard
@api_view(['GET'])
def admin_dashboard_summary(request):
    stats = User.objects.aggregate(
        num_of_users=Count('id'),
        num_of_females=Count('id', filter=Q(gender="Female")),
        num_of_males=Count('id', filter=Q(gender="Male")),
        num_of_staffs=Count('id', filter=Q(role="Staff")),
        num_of_admins=Count('id', filter=Q(role="Admin")),
        num_of_managers=Count('id', filter=Q(role="Manager")),
    )

    return Response({
        "num_of_users": stats['num_of_users'],
        "num_of_females": stats['num_of_females'],
        "num_of_males": stats['num_of_males'],
        "num_of_staffs": stats['num_of_staffs'],
        "num_of_admins": stats['num_of_admins'],
        "num_of_managers": stats['num_of_managers'],
    })


# display all user in the system in a table form



@api_view(['GET'])
def all_users_to_excel(request):
    users = User.objects.all()  # get all users
    serializer = api_ses.UserSerializerToExcel(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def all_users(request):
    users = User.objects.all().order_by('first_name', 'last_name')  # ordered queryset

    paginator = PageNumberPagination()
    result_page = paginator.paginate_queryset(users, request)

    serializer = api_ses.UserSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = api_ses.UserCreateSerializer
    permission_classes = [IsAuthenticated]  # remove if you want open access


# views.py
# for dynamic api options

class RegionList(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = api_ses.RegionSerializer

class DistrictList(generics.ListAPIView):
    queryset = Districts.objects.all()
    serializer_class = api_ses.DistrictSerializer

class DepartmentList(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = api_ses.DepartmentSerializer

class ClassesList(generics.ListAPIView):
    queryset = Classes.objects.all()
    serializer_class = api_ses.ClassesSerializer

class ManagementUnitList(generics.ListAPIView):
    queryset = ManagementUnit.objects.all()
    serializer_class = api_ses.ManagementUnitSerializer

class CurrentGradeList(generics.ListAPIView):
    queryset = CurrentGrade.objects.all()
    serializer_class = api_ses.CurrentGradeSerializer

class ChangeOfGradeList(generics.ListAPIView):
    queryset = ChangeOfGrade.objects.all()
    serializer_class = api_ses.ChangeOfGradeSerializer



# FOR THE USER MODEL FIELDS:
# fields to ignore
IGNORED_FIELDS = {
    "id", "password", "last_login", "is_superuser", "is_staff",
    "is_active", "date_joined", "groups", "user_permissions"
}
class UserFieldsAPIView(APIView):
    def get(self, request):
        fields = []
        for field in User._meta.get_fields():
            # skip reverse relations
            if field.auto_created and not field.concrete:
                continue

            # skip ignored fields
            if field.name in IGNORED_FIELDS:
                continue

            field_info = {
                "field_name": field.name,
                "field_type": field.get_internal_type(),
            }

            # include choices if available
            if getattr(field, "choices", None):
                field_info["choices"] = list(field.choices)

            # include items for ForeignKey
            if field.get_internal_type() == "ForeignKey":
                related_model = field.related_model
                queryset = related_model.objects.all()
                field_info["items"] = [
                    {"id": obj.id, "name": str(obj)} for obj in queryset
                ]
                field_info["multiple"] = False  # single select

            # include items for ManyToManyField
            if field.get_internal_type() == "ManyToManyField":
                related_model = field.related_model
                queryset = related_model.objects.all()
                field_info["items"] = [
                    {"id": obj.id, "name": str(obj)} for obj in queryset
                ]
                field_info["multiple"] = True  # multi-select

            fields.append(field_info)

        return Response(fields)

class UserFieldsAPIView(APIView):
    def get(self, request):
        fields = []
        for field in User._meta.get_fields():
            # skip reverse relations
            if field.auto_created and not field.concrete:
                continue

            # skip ignored fields
            if field.name in IGNORED_FIELDS:
                continue

            field_info = {
                "field_name": field.name,
                "field_type": field.get_internal_type(),
            }

            # include choices if available
            if getattr(field, "choices", None):
                field_info["choices"] = list(field.choices)

            # include items for ForeignKey
            if field.get_internal_type() == "ForeignKey":
                related_model = field.related_model
                queryset = related_model.objects.all()
                field_info["items"] = [{"id": obj.id, "name": str(obj)} for obj in queryset]

            # include items for ManyToManyField
            if field.get_internal_type() == "ManyToManyField":
                related_model = field.related_model
                queryset = related_model.objects.all()
                field_info["items"] = [{"id": obj.id, "name": str(obj)} for obj in queryset]

            fields.append(field_info)

        return Response(fields)

# user details per id for api

class UserDetailAPIView(APIView):
    def get(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        serializer = api_ses.UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    






from django.shortcuts import get_object_or_404
import logging

logger = logging.getLogger(__name__)

from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.shortcuts import get_object_or_404
import logging

logger = logging.getLogger(__name__)
# api_ses/views.py
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


class UserUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = api_ses.UserUpdateSerializer
    lookup_field = "pk"
    parser_classes = [MultiPartParser, FormParser, JSONParser]  # handles JSON + FormData

today = date.today()




from rest_framework import status
from urllib.parse import unquote  # For decoding URL-encoded strings

from django.db.models import Q
from datetime import date, timedelta

# Function to calculate date of birth range for a given age range
def get_birth_date_range(min_age, max_age):
    # Calculate the latest birth date (for the minimum age)
    max_date = today - timedelta(days=min_age * 365.25)  # Approx. years to days
    # Calculate the earliest birth date (for the maximum age)
    min_date = today - timedelta(days=(max_age + 1) * 365.25)  # +1 to include max_age
    return min_date, max_date



def get_birth_date_range(min_age, max_age):
    today = date.today()
    max_date = today - timedelta(days=min_age * 365.25)
    min_date = today - timedelta(days=max_age * 365.25)
    return min_date, max_date

@api_view(["GET"])
def users_per_department(request):
    dept = unquote(request.GET.get("dept", "")).strip()

    # Reference lists
    total_dpts = Department.objects.values_list("department_name", flat=True)
    total_cls = Classes.objects.values_list("classes_name", flat=True)
    total_rgn = Region.objects.values_list("region", flat=True)
    total_mng_unit = ManagementUnit.objects.values_list("management_unit_name", flat=True)

    total_staff = [choice[0] for choice in User.STAFF_CHOICES]
    total_gen = [choice[0] for choice in User.GENDER_CHOICES]
    total_leave = [choice[0] for choice in User.ON_LEAVE_TYPE_CHOICES]
    total_full = [choice[0] for choice in User.CONTRACT_FULLTIME]

    age_ranges = {
        "20 - 30": (20, 30),
        "31 - 40": (31, 40),
        "41 - 50": (41, 50),
        "51 - 60": (51, 60),
        "61+": (61, 100),
    }

    salary_ranges = {f"SS.{i}": f"SS.{i}" for i in range(5, 26)}

    users = User.objects.none()
    filter_key = None

    try:
        if dept in total_dpts:
            users = User.objects.filter(directorate__department_name__iexact=dept)
            filter_key = "department"
        elif dept in total_cls:
            users = User.objects.filter(category__classes_name__iexact=dept)
            filter_key = "class"
        elif dept in total_rgn:
            users = User.objects.filter(region__region__iexact=dept)
            filter_key = "region"
        elif dept in total_mng_unit:
            users = User.objects.filter(management_unit_cost_centre__management_unit_name__iexact=dept)
            filter_key = "unit"
        elif dept in total_staff:
            users = User.objects.filter(staff_category=dept)
            filter_key = "staff category"
        elif dept in total_gen:
            users = User.objects.filter(gender=dept)
            filter_key = "gender category"
        elif dept in age_ranges:
            min_age, max_age = age_ranges[dept]
            min_date, max_date = get_birth_date_range(min_age, max_age)
            users = User.objects.filter(
                date_of_birth__gte=min_date,
                date_of_birth__lte=max_date,
                date_of_birth__isnull=False
            )
            filter_key = "age range"
        elif dept in salary_ranges:
            users = User.objects.filter(current_salary_level=dept)
            filter_key = "salary range"
        elif dept in total_leave:
            users = User.objects.filter(on_leave_type=dept)
            filter_key = "leave type"
        elif dept in total_full:
            users = User.objects.filter(fulltime_contract_staff=dept)
            filter_key = "agreement type"
        elif dept in ["Professional", "Subprofessional"]:
            users = User.objects.filter(professional=dept)
            filter_key = "professional type"

        # Pagination
        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(users, request)

        serializer = api_ses.UserSerializer(result_page, many=True)

        # Filter out unwanted fields
        filtered_users = [
            {key: user[key] for key in user if key not in ["staff_category", "districts"]}
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
    dept = unquote(request.GET.get("dept", "")).strip()

    # Reference lists
    total_dpts = Department.objects.values_list("department_name", flat=True)
    total_cls = Classes.objects.values_list("classes_name", flat=True)
    total_rgn = Region.objects.values_list("region", flat=True)
    total_mng_unit = ManagementUnit.objects.values_list("management_unit_name", flat=True)

    total_staff = [choice[0] for choice in User.STAFF_CHOICES]
    total_gen = [choice[0] for choice in User.GENDER_CHOICES]
    total_leave = [choice[0] for choice in User.ON_LEAVE_TYPE_CHOICES]
    total_full = [choice[0] for choice in User.CONTRACT_FULLTIME]

    age_ranges = {
        "20 - 30": (20, 30),
        "31 - 40": (31, 40),
        "41 - 50": (41, 50),
        "51 - 60": (51, 60),
        "61+": (61, 100),
    }

    salary_ranges = {f"SS.{i}": f"SS.{i}" for i in range(5, 26)}

    users = User.objects.none()
    filter_key = None

    try:
        if dept in total_dpts:
            users = User.objects.filter(directorate__department_name__iexact=dept)
            filter_key = "department"
        elif dept in total_cls:
            users = User.objects.filter(category__classes_name__iexact=dept)
            filter_key = "class"
        elif dept in total_rgn:
            users = User.objects.filter(region__region__iexact=dept)
            filter_key = "region"
        elif dept in total_mng_unit:
            users = User.objects.filter(management_unit_cost_centre__management_unit_name__iexact=dept)
            filter_key = "unit"
        elif dept in total_staff:
            users = User.objects.filter(staff_category=dept)
            filter_key = "staff category"
        elif dept in total_gen:
            users = User.objects.filter(gender=dept)
            filter_key = "gender category"
        elif dept in age_ranges:
            min_age, max_age = age_ranges[dept]
            min_date, max_date = get_birth_date_range(min_age, max_age)
            users = User.objects.filter(
                date_of_birth__gte=min_date,
                date_of_birth__lte=max_date,
                date_of_birth__isnull=False
            )
            filter_key = "age range"
        elif dept in salary_ranges:
            users = User.objects.filter(current_salary_level=dept)
            filter_key = "salary range"
        elif dept in total_leave:
            users = User.objects.filter(on_leave_type=dept)
            filter_key = "leave type"
        elif dept in total_full:
            users = User.objects.filter(fulltime_contract_staff=dept)
            filter_key = "agreement type"
        elif dept in ["Professional", "Subprofessional"]:
            users = User.objects.filter(professional=dept)
            filter_key = "professional type"

        # No pagination – just serialize all results
        serializer = api_ses.UserSerializer(users, many=True)

        # Filter out unwanted fields
        filtered_users = [
            {key: user[key] for key in user if key not in ["staff_category", "districts"]}
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
