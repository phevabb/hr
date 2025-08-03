from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from .forms import Login_form
from django.contrib.auth import authenticate, login

from django.contrib.auth import get_user_model

User = get_user_model()




def display_login_page(request):
    form = Login_form()
    context = {"form": form}
    return render(request, "registration/login.html", context)

# Create your views here.
@sensitive_post_parameters()
@csrf_protect
@never_cache
def login_view(request):
    next_url = request.GET.get("next", "")
    if request.method == "POST":
        form: Login_form = Login_form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            staff_department = request.POST["staff_department"]
            user_ID = request.POST["user_ID"]
            user = authenticate(request, user_id=cd["user_ID"], password=cd["password"])

            if user is not None:
                if user.is_active:
                    login(request, user)



                    #  FOR Admin
                    if staff_department == "Admin":
                        admin_ = User.objects.filter(user_id__icontains=user_ID)


                        if admin_:
                            return redirect(next_url or "superadmin:dashboard")
                        else:
                            messages.error(
                                request, "please select appropriate department"
                            )
                            return redirect("display_login_page")







                else:
                    return HttpResponse("Disabled Account")
            else:
                messages.error(request, "Invalid login")
                return redirect("display_login_page")
                # return HttpResponse('Invalid login')
    else:
        form = Login_form()

    return render(request, "registration/login.html", {"form": form})