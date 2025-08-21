from django.db import models

# Create your models here.



class User(models.Model):
    user_email=models.EmailField(unique=True)
    user_password=models.CharField(max_length=255)


class Session(models.Model):
    token=models.CharField(max_length=64,unique=True)
    user_email=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)



