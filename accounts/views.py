from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from .models import User,Session
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password,check_password
import uuid

# Create your views here.

import json

@csrf_exempt
def register(request):
    if request.method=="POST":
        data=json.loads(request.body)

        user_email=data.get('user_email')
        user_password=data.get('user_password')

        if User.objects.filter(user_email=user_email).exists():
            return JsonResponse({"error":"user already exist"},status=400)

        User.objects.create(user_email=user_email,user_password=make_password(user_password))

        user=User.objects.get(user_email=user_email)

        token=str(uuid.uuid4())

        Session.objects.create(user_email=user,token=token)

        return JsonResponse({"message":"success","token":token},status=200)
    else:
        return JsonResponse({"error":"post required"},status=404)




@csrf_exempt
def login(request):
    if request.method=="POST":
        data=json.loads(request.body)

        user_email=data.get('user_email')
        user_password=data.get('user_password')

        user=User.objects.filter(user_email=user_email).first()
        if not user:
            return JsonResponse({"error":"user does not exist"},status=400)

        if not check_password(user_password,user.user_password):
            return JsonResponse({"error":"wrong password"},status=400)

        # remove old token
        old_token=Session.objects.filter(user_email=user_email).first()
        if old_token:
            old_token.delete()

        token=str(uuid.uuid4())
        Session.objects.create(user_email=user_email,token=token)

        return JsonResponse({"message":"success","token":token},status=200)
    else:
        return JsonResponse({"error":"post required"},status=404)

def page(request):
    return render(request,'auth.html')