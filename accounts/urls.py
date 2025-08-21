from . import views
from django.urls import path

urlpatterns = [
    path('',views.page,name='page'),
    path('register',views.register,name='register'),
    
]
