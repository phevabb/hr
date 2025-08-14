
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.generic import View
from account.forms import UserForm  # Import your form
import json
from django.shortcuts import render
from account.models import User, Department, Classes, Region, ManagementUnit


# Create your views here.


def all_users(request):
    users = User.objects.all()
    paginator = Paginator(users, 10)  # 10 patients per page
    page = request.GET.get('page', 1)
    posts = paginator.get_page(page)
    context = {"posts": posts}
    return render(request, 'superadmin/users.html', context)


def new_entry(request):
    return render(request, 'superadmin/new_entry.html')




class UserCreateView(View):
    template_name = 'superadmin/new_entry.html'  # Your template path

    def get(self, request, *args, **kwargs):
        form = UserForm()  # Create empty form for GET request
        return render(request, self.template_name, {'form': form, 'edit': "New Entry"})

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)  # Bind form with POST data

        if form.is_valid():
            # Save the form (this will use default password if none provided)
            user = form.save()

            # Redirect to success page or user detail view
            return redirect('superadmin:dashboard')  # Change to your success URL name

        # If form is invalid, re-render the form with errors
        return render(request, self.template_name, {'form': form})


# For editing existing users
class UserUpdateView(View):
    template_name = 'superadmin/new_entry.html'  # Your template path

    def get(self, request, pk, *args, **kwargs):
        user = User.objects.get(pk=pk)  # Get the user instance
        form = UserForm(instance=user)  # Pre-populate form with user data
        return render(request, self.template_name, {'form': form, 'user': user, 'edit': "Edit User"})

    def post(self, request, pk, *args, **kwargs):
        user = User.objects.get(pk=pk)
        form = UserForm(request.POST, instance=user)  # Bind form with POST data and instance

        if form.is_valid():
            form.save()  # Save the changes
            return redirect('superadmin:dashboard')  # Change to your success URL name

        # If form is invalid, re-render the form with errors
        return render(request, self.template_name, {'form': form, 'user': user})


class UserDetailView(View):
    template_name = 'superadmin/user_detail.html'  # Your template path

    def get(self, request, pk, *args, **kwargs):
        user = User.objects.get(pk=pk)  # Get the user instance
        full_name = user.full_name
        title = user.title
        form = UserForm(instance=user)  # Pre-populate form with user data
        return render(request, self.template_name, {'title':title,'full_name':full_name,'form': form, 'user': user, 'edit': "Edit User"})

# Analysis of Staff Distribution
def index(request):
    users = User.objects.all()
    # FOR DEPARTMENT / DIRECTORATE
    # Get all users with directorate data pre-fetched (optimized query)
    user_queryset = User.objects.all().select_related('directorate')
    # Initialize department counts with all possible departments set to 0
    all_departments = Department.objects.all()
    department_counts = {dept.department_name: 0 for dept in all_departments}
    # Count users by directorate
    for user in user_queryset:
        if user.directorate:
            department_name = user.directorate.department_name
            department_counts[department_name] += 1
    # Prepare data for both chart and table (same as before)
    departments_list = list(department_counts.keys())
    counts_list = list(department_counts.values())
    num_of_departments = len(departments_list)
    # Combined data for table display (same as before)
    department_data = list(zip(departments_list, counts_list))





    # FOR CLASS / CATEGORY
    # Fetch all users with their related category to avoid extra queries
    user_queryset = User.objects.all().select_related('category')
    # Initialize counts for all possible classes
    all_classes = Classes.objects.all()
    classes_count = {cls.classes_name: 0 for cls in all_classes}

    # Count users in each class
    for user in user_queryset:
        if user.category:
            classes_name = user.category.classes_name
            classes_count[classes_name] += 1

    # Prepare data for charts and tables
    class_keys = list(classes_count.keys())
    class_values = list(classes_count.values())
    num_of_class = len(class_keys)  # number of unique classes

    # Combined data for table display
    class_data = list(zip(class_keys, class_values))





    # c) Total number of Senior & Junior Staff
    senior_junior_staff = {choice[0]: 0 for choice in User.STAFF_CHOICES}
    for user in users:
        if user.staff_category:
            try:
                senior_junior_staff[user.staff_category] += 1
            except Exception as e:
                print(f"Error processing user: {user} with staff_category: {user.staff_category}")
                print(f"Exception: {e}")

    senior_junior_staff_keys = list(senior_junior_staff.keys())
    senior_junior_staff_values = list(senior_junior_staff.values())
    num_of_senior_junior_staff = len(senior_junior_staff_values)

    senior_junior_staff_data = list(zip(senior_junior_staff_keys, senior_junior_staff_values))

    # FOR REGION
    # Fetch all users with related region to avoid extra queries
    user_queryset = User.objects.all().select_related('region')

    # Initialize counts for all possible regions
    all_regions = Region.objects.all()
    region_count = {reg.region: 0 for reg in all_regions}

    # Count users in each region
    for user in user_queryset:
        if user.region:
            region_name = user.region.region
            region_count[region_name] += 1

    # Prepare data for charts and tables
    region_keys = list(region_count.keys())
    region_values = list(region_count.values())
    num_of_region = len(region_keys)  # number of unique regions

    # Combined data for table display
    region_data = list(zip(region_keys, region_values))





    # contract
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
    contract_data = list(zip(contract_keys, contract_values))


    # FOR LEAVE TYPE
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
    on_leave_data = list(zip(on_leave_keys, on_leave_values))

    # FOR MANAGEMENT UNIT / COST CENTRE
    # Fetch all users with related management unit
    user_queryset = User.objects.all().select_related('management_unit_cost_centre')

    # Initialize counts for all management units
    all_management_units = ManagementUnit.objects.all()
    management_count = {mu.management_unit_name: 0 for mu in all_management_units}

    # Count users in each management unit
    for user in user_queryset:
        if user.management_unit_cost_centre:
            unit_name = user.management_unit_cost_centre.management_unit_name
            management_count[unit_name] += 1

    # Prepare data for charts and tables
    m_keys = list(management_count.keys())
    m_values = list(management_count.values())
    num_of_management = len(m_keys)

    # Combined data for table display
    management_data = list(zip(m_keys, m_values))





    # FOR GENDER
    gender_count = {choice[0]: 0 for choice in User.GENDER_CHOICES}
    for user in users:
        if user.gender:
            gender_count[user.gender] += 1

    gender_keys = list(gender_count.keys())
    gender_values = list(gender_count.values())
    num_of_gender = len(gender_values)
    gender_data = list(zip(gender_keys, gender_values))


    # for professionals
    pros = 0
    sub_pros = 0

    for user in users:
        if user.professional_qualification:
            pros = pros + 1

        else:
            sub_pros = sub_pros + 1



    # FOR AGE RANGE
    age_ranges = {
        '0 - 20': 0,
        '21 - 40': 0,
        '41 - 60': 0,
        '60+': 0
    }

    for user in users:
        if user.age is not None:
            if 0 <= user.age <= 20:
                age_ranges['0 - 20'] += 1
            elif 21 <= user.age <= 40:
                age_ranges['21 - 40'] += 1
            elif 41 <= user.age <= 60:
                age_ranges['41 - 60'] += 1
            elif user.age > 60:
                age_ranges['60+'] += 1

    age_keys = list(age_ranges.keys())
    age_values = list(age_ranges.values())
    num_of_age_ranges = len(age_values)
    age_data = list(zip(age_keys, age_values))

    # FOR SALARY LEVEL RANGE
    salary_range_counts = {
        'SS.1 - SS.10': 0,
        'SS.11 - SS.15': 0,
        'SS.16 - SS.20': 0,
        'SS.21+': 0
    }

    for user in users:
        if user.current_salary_level:
            try:
                # Extract the numeric level from strings like 'SS.16'
                level = int(user.current_salary_level.replace('SS.', '').strip())

                if 1 <= level <= 10:
                    salary_range_counts['SS.1 - SS.10'] += 1
                elif 11 <= level <= 15:
                    salary_range_counts['SS.11 - SS.15'] += 1
                elif 16 <= level <= 20:
                    salary_range_counts['SS.16 - SS.20'] += 1
                elif level >= 21:
                    salary_range_counts['SS.21+'] += 1

            except ValueError:
                print(f"Invalid salary level: {user.current_salary_level}")



    salary_range_keys = list(salary_range_counts.keys())
    salary_range_values = list(salary_range_counts.values())
    num_of_salary_ranges = len(salary_range_values)
    salary_range_data = list(zip(salary_range_keys, salary_range_values))

    context = {
        'all_users': users.count(),
        'females': User.objects.filter(gender="Female").count(),
        'males': User.objects.filter(gender="Male").count(),
        'staff': User.objects.filter(role="Staff").count(),
        'admins': User.objects.filter(role="Admin").count(),
        'managers': User.objects.filter(role="Manager").count(),

        # salary level
        'num_of_salary_ranges':num_of_salary_ranges,
        'salary_range_data':salary_range_data,

        # FOR CONTRACT
        'contract_data':contract_data,
        'num_of_contract':num_of_contract,

        # for pros
        'pros':pros,
        'sub_pros':sub_pros,

        # FOR AGE
        'num_of_age':num_of_age_ranges,
        'age_data':age_data,

        # FOR GENDER
        'num_of_gender':num_of_gender,
        'gender_data':gender_data,

        # for on leave
        'num_of_on_leave':num_of_on_leave,
        'on_leave_data': on_leave_data,



        # FOR DIRECTORATE
        'num_of_departments':num_of_departments,
        'department_data': department_data,

        # FOR MANAGEMENT
        'num_of_management':num_of_management,
        'management_data': management_data,

        # FOR DISTRICT
        'num_of_region':num_of_region,
        'region_data': region_data,



        # FOR CLASS
        'num_of_class': num_of_class,
        'class_data': class_data,

        # For senior junior staff
        'senior_junior_staff_data':senior_junior_staff_data,
        'num_of_senior_junior_staff':num_of_senior_junior_staff,



        'total_users': users.count(),
    }
    return render(request, 'superadmin/dashboard.html', context)


def distribution(request):
    users = User.objects.all()
    #

    return None


def movement():
    return None


def training():
    return None