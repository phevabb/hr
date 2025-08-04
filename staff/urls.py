from django.urls import path
from.views import index

app_name = 'staff'

urlpatterns = [
    path('',index,name='dashboard' ),

]