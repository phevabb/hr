
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.generic import View
from account.forms import UserForm  # Import your form
import json
from django.shortcuts import render
from account.models import User

def index(request):
    users = User.objects.all()


    # FOR DIRECTORATE
    # Initialize department counts with all possible choices set to 0
    department_counts = {choice[0]: 0 for choice in User.DEPARTMENT_CHOICES}

    # Count users by directorate
    for user in users:
        if user.directorate:
            department_counts[user.directorate] += 1

    # Prepare data for both chart and table
    departments_list = list(department_counts.keys())
    counts_list = list(department_counts.values())
    num_of_departments = len(departments_list)

    # ✅ Combined data for table display
    department_data = list(zip(departments_list, counts_list))


    # FOR CLASS / CATEGORY
    class_count = {choice[0]: 0 for choice in User.CLASS_CHOICES}
    for user in users:
        if user.category:
            class_count[user.category] += 1

    class_keys = list(class_count.keys())
    class_values = list(class_count.values())
    num_of_class = len(class_values)

    class_data = list(zip(class_keys, class_values))


    # FOR REGION
    region_count = {choice[0]: 0 for choice in User.REGION_CHOICES}
    for user in users:
        if user.region:
            region_count[user.region] += 1

    region_keys = list(region_count.keys())
    region_values = list(region_count.values())
    num_of_region = len(region_values)
    region_data = list(zip(region_keys, region_values))

    # FOR MANAGEMENT
    management_count = {choice[0]:0 for choice in User.MANAGEMENT_UNIT_CHOICES}
    for user in users:
        if user.management_unit_cost_centre:
            management_count[user.management_unit_cost_centre] += 1

    m_keys = list(management_count.keys())
    m_values = list(management_count.values())
    num_of_management = len(m_values)
    management_data = list(zip(m_keys, m_values))

    context = {
        'all_users': users.count(),
        'females': User.objects.filter(gender="Female").count(),
        'males': User.objects.filter(gender="Male").count(),
        'staff': User.objects.filter(role="Staff").count(),
        'admins': User.objects.filter(role="Admin").count(),
        'managers': User.objects.filter(role="Manager").count(),

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


        'total_users': users.count(),
    }
    return render(request, 'superadmin/dashboard.html', context)



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

