from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response    
from django.contrib.auth import get_user_model
from account.models import User, Department, Classes, Region, ManagementUnit
from django.db.models import Count, Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .ses import UserCreateSerializer
from rest_framework import generics
from account.models import Region, Districts, Department, Classes, ManagementUnit, CurrentGrade, ChangeOfGrade
from superadmin.api import ses as api_ses
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from account.models import User, Department, Classes, Districts, Region, CurrentGrade, ChangeOfGrade, ManagementUnit





User = get_user_model()
users = User.objects.all()


# Analysis of Staff Distribution API
# directorate stats
@api_view(['GET'])
def department_stats(request):
    user_queryset = User.objects.select_related('directorate').all()

    # Initialize all departments with 0
    all_departments = Department.objects.all()
    department_counts = {dept.department_name: 0 for dept in all_departments}


    # count user in each department
    for user in user_queryset:
        if user.directorate:
            department_name = user.directorate.department_name
            department_counts[department_name]+=1

    # convert to lists to be used in tables
    department_list = list(department_counts.keys())
    counts_list = list(department_counts.values())
    num_of_departments = len(department_list)

    # table format
    department_data = [
        {"department":dept, "count":count}
        for dept, count in department_counts.items()
    ]

    return Response({
        "name_": "Directorates",
        "departments": department_list,
        "counts": counts_list,
        "num_of_departments": num_of_departments,
        "table_data": department_data
    })


# class stats
@api_view(['GET'])
def class_stats(request):
    user_queryset = User.objects.select_related('category').all()
    all_classes = Classes.objects.all()
    # Initialize all classes with 0
    class_counts = {cls.classes_name: 0 for cls in all_classes}
    for user in user_queryset:
        if user.category:
            class_name = user.category.classes_name
            class_counts[class_name] += 1
    
    # convert to lists to be used in tables
    class_list = list(class_counts.keys())
    count_list = list(class_counts.values())
    num_of_classes = len(class_list)
    # table format
    class_data = [
        {"class":cls, "count":count}
        for cls, count in class_counts.items()
    ]

    return Response({
        "name_": "Classes",
        "classes": class_list,
        "counts": count_list,
        "num_of_classes": num_of_classes,
        "table_data": class_data
    })

# region stats
@api_view(['GET'])
def region_stats(request):
    user_queryset = User.objects.select_related('region').all()
    #initialize all regions with 0
    all_regions = Region.objects.all()
    region_count = {reg.region: 0 for reg in all_regions}
    # count users in each region
    for user in user_queryset:
        if user.region:
            region_name = user.region.region
            region_count[region_name] += 1
    
    # convert to lists to be used in tables
    region_list = list(region_count.keys())
    count_list = list(region_count.values())
    num_of_regions = len(region_list)
    # table format
    region_data = [
        {"region":reg, "count":count}
        for reg, count in region_count.items()
    ]

    return Response({
        "name_": "Regions",
        "regions": region_list,
        "counts": count_list,
        "num_of_regions": num_of_regions,
        "table_data": region_data
    })


# management stats
@api_view(['GET'])
def management_stats(request):
    user_queryset = User.objects.select_related('management_unit_cost_centre').all()
    #initialize all management units with 0
    all_management_units = ManagementUnit.objects.all()
    management_count = {mu.management_unit_name: 0 for mu in all_management_units}
    # count users in each management unit
    for user in user_queryset:
        if user.management_unit_cost_centre:
            mu_name = user.management_unit_cost_centre.management_unit_name
            management_count[mu_name] += 1    
    # convert to lists to be used in tables
    management_list = list(management_count.keys())
    count_list = list(management_count.values())
    num_of_management_units = len(management_list)
    # table format
    management_data = [
        {"management_unit":mu, "count":count}
        for mu, count in management_count.items()
    ]

    return Response({ 
        "name_": "Management Units",
        "management_units": management_list,
        "counts": count_list,
        "num_of_management_units": num_of_management_units,
        "table_data": management_data
    })


# Gender stats
@api_view(['GET'])
def gender_stats(request):
    gender_count = {choice[0]: 0 for choice in User.GENDER_CHOICES}
    for user in users:
        if user.gender:
            gender_count[user.gender] += 1

    # convert to lists to be used in tables
    gender_list = list(gender_count.keys())
    count_list = list(gender_count.values())
    num_of_genders = len(gender_list)
    
    # table format
    gender_data = [
        {"gender":gen, "count":count}
        for gen, count in gender_count.items()
    ]

    return Response({
        "name_": "Gender",
        "gender_list": gender_list,
        "counts": count_list,
        "num_of_genders": num_of_genders,
        "table_data": gender_data,
    })

# age stats
@api_view(['GET'])
def age_stats(request):
    age_ranges = {
        '20 - 30': 0,
        '31 - 40': 0,
        '41 - 50': 0,
        '51 - 60': 0,
        '61+': 0
    }
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
            elif user.age > 61:
                age_ranges['61+'] += 1
    
    # convert to lists to be used in tables
    age_list = list(age_ranges.keys())
    count_list = list(age_ranges.values())
    num_of_age_ranges = len(age_list)

    # table format
    age_data = [
        {"age_range":age_range, "count":count}
        for age_range, count in age_ranges.items()
    ]

    return Response({
        "name_": "Age Distribution",
        "age_ranges": age_list,
        "counts": count_list,
        "num_of_age_ranges": num_of_age_ranges,
        "table_data": age_data
    })

# grade level
@api_view(['GET'])
def grade_level_stats(request):
    salary_range_count = {
        "SS.25":0,
        "SS.24":0,
        "SS.23":0,
        "SS.22":0,
        "SS.21":0,
        "SS.20":0,
        "SS.19":0,
        "SS.18":0,
        "SS.17":0,
        "SS.16":0,
        "SS.15":0,
        "SS.14":0,
        "SS.13":0,
        "SS.12":0,
        "SS.11":0,
        "SS.10":0,
        "SS.9":0,
        "SS.8":0,  
        "SS.7":0,
        "SS.6":0,
        "SS.5":0,
    }

    for user in users:
        if user.current_salary_level:
            try:
                salary_range_count[user.current_salary_level] += 1
            except Exception as e:
                print(f"Error:, {e}")

    # convert to lists to be used in tables
    salary_range_list = list(salary_range_count.keys())
    count_list = list(salary_range_count.values())
    num_of_salary_ranges = len(salary_range_list)

    # table format
    salary_range_data = [
        {"salary_range":sr, "count":count}
        for sr, count in salary_range_count.items()
    ]   

    return Response({
        "name_": "Grade Levels",
        "salary_ranges": salary_range_list,
        "counts": count_list,
        "num_of_salary_ranges": num_of_salary_ranges,
        "table_data": salary_range_data 
    })


# leave type stats
@api_view(['GET'])
def leave_type_stats(request):
    on_leave_count = {choice[0]: 0 for choice in User.ON_LEAVE_TYPE_CHOICES}
    for user in users:

        try:
            if user.on_leave_type:
                on_leave_count[user.on_leave_type] += 1

        except ValueError:
            print(f"Invalid salary level: {user.on_leave_type} {user}")




    on_leave_keys = list(on_leave_count.keys())
    on_leave_values = list(on_leave_count.values())
    num_of_on_leave = len(on_leave_values)
    # table format
    on_leave_data = [
        {"leave_type":lt, "count":count}
        for lt, count in on_leave_count.items()
    ]       

    return Response({
        "name_": "On Leave Types",
        "leave_types": on_leave_keys,
        "counts": on_leave_values,
        "num_of_on_leave": num_of_on_leave,
        "table_data": on_leave_data
    })
        

# contract stats
@api_view(['GET'])
def contract_stats(request):
    contract_count = {choice[0]: 0 for choice in User.CONTRACT_FULLTIME}
    for user in users:
        try:
            if user.fulltime_contract_staff:
                contract_count[user.fulltime_contract_staff] += 1
        except Exception as e:
            print(f"the full time problem: {e} {user}")
    contract_keys = list(contract_count.keys())
    contract_values = list(contract_count.values())
    num_of_contract = len(contract_values)

    # for table
    contract_data = [
        {"contract_type":ct, "count":count}
        for ct, count in contract_count.items()
        ]
    return Response({
        "name_": "Contract Types",  
        "contract_types": contract_keys,
        "counts": contract_values,
        "num_of_contract": num_of_contract,
        "table_data": contract_data 
    })  


# senior stats
@api_view(['GET'])
def senior_stats(request):
    senior_junior_staff = {choice[0]: 0 for choice in User.STAFF_CHOICES}
    for user in users:
        if user.staff_category:
            try:
                senior_junior_staff[user.staff_category] += 1
            except Exception as e:
                print(f"Error:, {e}")
    # convert to lists to be used in tables
    staff_category_list = list(senior_junior_staff.keys())
    count_list = list(senior_junior_staff.values())     
    num_of_categories = len(staff_category_list)

    # table format
    staff_category_data = [
        {"staff_category":cat, "count":count}
        for cat, count in senior_junior_staff.items()
    ]

    return Response({
        "name_": "Senior/Junior Staff",
        "staff_categories": staff_category_list,
        "counts": count_list,
        "num_of_categories": num_of_categories,
        "table_data": staff_category_data
    })

# pro stats
@api_view(['GET'])
def pro_stats(request):

    professional_count = {choice[0]: 0 for choice in User.PROFESSIONAL_CHOICES}
    for user in users:
        if user.professional:
            try:
                professional_count[user.professional] += 1
            except Exception as e:
                print(f"Error:, {e}")
        
        # convert to lists to be used in tables
    pro_list = list(professional_count.keys())  
    count_list = list(professional_count.values())
    num_of_pros = len(pro_list)
    # table format
    pro_data = [
        {"professional":pro, "count":count}
        for pro, count in professional_count.items()
    ]   

    return Response({
        "name_": "Professionals and Sub Professionals",  
        "professionals": pro_list,
        "counts": count_list,
        "num_of_pros": num_of_pros,
        "table_data": pro_data 
    })  


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

from rest_framework.pagination import PageNumberPagination

from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10  # default, can still be overridden by ?page_size=

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'page_size': self.page_size,  # <--- added here
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def all_users_to_excel(request):
    users = User.objects.all()  # get all users
    serializer = api_ses.UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def all_users(request):
    users = User.objects.all()  # your queryset
    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(users, request)

    # Serialize the paginated users
    serializer = api_ses.UserSerializer(result_page, many=True)

    return paginator.get_paginated_response(serializer.data)
# new entry (creating a new user)
class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = api_ses.UserCreateSerializer
    # remove this if you want open access
    permission_classes = [IsAuthenticated]

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
                field_info["items"] = [{"id": obj.id, "name": str(obj)} for obj in queryset]

            fields.append(field_info)

        return Response(fields)
    
# user details per id for api
class UserDetailAPIView(APIView):
    def get(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        serializer = api_ses.UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserUpdateAPIView(APIView):
    def get(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        serializer = api_ses.UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        print(f'here is put data from frontend{request.data}')
        serializer = api_ses.UserSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        print(f'here is patch data from frontend{request.data}')
        serializer = api_ses.UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#number of users by department / unit
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status




from rest_framework import status
from urllib.parse import unquote  # For decoding URL-encoded strings




@api_view(["GET"])
def users_by_department(request):
    # Decode the dept parameter to handle URL-encoded characters
    dept = unquote(request.GET.get("dept", "")).strip()

    # Debugging: Print the decoded dept value
    print(f"Received dept: '{dept}'")

    # Get reference lists
    total_dpts = Department.objects.values_list("department_name", flat=True)
    for i in total_dpts:
        print(f"Department in DB: '{i}'")
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
        "61+": (61, None),
    }

    salary_ranges = {
        "SS.1 - SS.10": (1, 10),
        "SS.11 - SS.15": (11, 15),
        "SS.16 - SS.20": (16, 20),
        "SS.21+": (21, None),
    }

    users = User.objects.none()
    filter_key = None

    try:
        # Department
        if dept in total_dpts:
            users = User.objects.filter(directorate__department_name__iexact=dept)
            filter_key = "department"

        # Class
        elif dept in total_cls:
            users = User.objects.filter(category__classes_name__iexact=dept)
            filter_key = "class"

        # Region
        elif dept in total_rgn:
            users = User.objects.filter(region__region__iexact=dept)
            filter_key = "region"

        # Management Unit
        elif dept in total_mng_unit:
            users = User.objects.filter(management_unit_cost_centre__management_unit_name__iexact=dept)
            filter_key = "unit"

        # Staff Category
        elif dept in total_staff:
            users = User.objects.filter(staff_category=dept)
            filter_key = "staff category"

        # Gender
        elif dept in total_gen:
            users = User.objects.filter(gender=dept)
            filter_key = "gender category"

        # Age Range
        elif dept in age_ranges:
            min_age, max_age = age_ranges[dept]
            if max_age:
                users = User.objects.filter(age__gte=min_age, age__lte=max_age)
            else:
                users = User.objects.filter(age__gte=min_age)
            filter_key = "age range"

        # Salary Range
        elif dept in salary_ranges:
            min_level, max_level = salary_ranges[dept]
            all_users = User.objects.exclude(current_salary_level__isnull=True)
            filtered_users = []
            for user in all_users:
                try:
                    level = int(user.current_salary_level.replace("SS.", "").strip())
                    if max_level is None and level >= min_level:
                        filtered_users.append(user)
                    elif min_level <= level <= max_level:
                        filtered_users.append(user)
                except (ValueError, AttributeError):
                    continue
            users = filtered_users
            filter_key = "salary range"

        # Leave Type
        elif dept in total_leave:
            users = User.objects.filter(on_leave_type=dept)
            filter_key = "leave type"

        # Fulltime/Contract
        elif dept in total_full:
            users = User.objects.filter(fulltime_contract_staff=dept)
            filter_key = "agreement type"

        # Professional / Sub Professional
        elif dept in ["PROFESSIONAL", "SUB PROFESSIONAL"]:
            users = User.objects.filter(professional=dept)
            filter_key = "professional type"

        # Serialize results
        serializer = api_ses.UserSerializer(users, many=True)

        # Filter out unwanted fields (staff_category, districts) in the response
        filtered_users = [
            {
                key: user[key]
                for key in user
                if key not in ["staff_category", "districts"]
            }
            for user in serializer.data
        ]

        return Response(
            {
                "dept": dept,
                "filter_type": filter_key,
                "count": len(filtered_users),
                "users": filtered_users,
            },
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        print(f"Error: {str(e)}")
        return Response(
            {
                "dept": dept,
                "filter_type": None,
                "count": 0,
                "users": [],
                "error": str(e),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    