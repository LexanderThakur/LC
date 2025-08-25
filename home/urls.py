from . import views
from django.urls import path

urlpatterns = [
    path('',views.page,name="page"),
    path('submit_link/',views.submit_link,name="submit_link"),
    path('get_link/',views.get_link,name="get_link"),
    
]
