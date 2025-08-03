from django.urls import path
from.views import index

app_name = 'superadmin'

urlpatterns = [
    path('',index,name='dashboard' ),

]