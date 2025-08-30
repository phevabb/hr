from rest_framework.decorators import api_view
from rest_framework.response import Response    
from django.contrib.auth import get_user_model
from account.models import User, Department, Classes, Region, ManagementUnit



User = get_user_model()


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

    