from django.core.paginator import Paginator
from django.shortcuts import render

from account.models import User


# Create your views here.

def index(request):
    all_users_ = User.objects.all()
    all_users_= all_users_.count()
    context = {'all_users':all_users_}
    return render(request, 'superadmin/dashboard.html', context)


def all_users(request):
    users = User.objects.all()
    paginator = Paginator(users, 10)  # 10 patients per page
    page = request.GET.get('page', 1)
    posts = paginator.get_page(page)
    context = {"posts": posts}
    return render(request, 'superadmin/users.html', context)


def new_entry(request):
    return render(request, 'superadmin/new_entry.html')


from django.shortcuts import render, redirect
from django.views.generic import View
from account.forms import UserForm  # Import your form
from account.models import User  # Import your User model


class UserCreateView(View):
    template_name = 'superadmin/new_entry.html'  # Your template path

    def get(self, request, *args, **kwargs):
        form = UserForm()  # Create empty form for GET request
        return render(request, self.template_name, {'form': form})

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
    template_name = 'users/edit_user.html'  # Your template path

    def get(self, request, pk, *args, **kwargs):
        user = User.objects.get(pk=pk)  # Get the user instance
        form = UserForm(instance=user)  # Pre-populate form with user data
        return render(request, self.template_name, {'form': form, 'user': user})

    def post(self, request, pk, *args, **kwargs):
        user = User.objects.get(pk=pk)
        form = UserForm(request.POST, instance=user)  # Bind form with POST data and instance

        if form.is_valid():
            form.save()  # Save the changes
            return redirect('user_detail', pk=user.pk)  # Change to your success URL name

        # If form is invalid, re-render the form with errors
        return render(request, self.template_name, {'form': form, 'user': user})
