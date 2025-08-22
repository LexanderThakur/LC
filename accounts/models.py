from django.db import models

# Create your models here.



class User(models.Model):
    user_email=models.EmailField(unique=True)
    user_password=models.CharField(max_length=255)


class Session(models.Model):
    token=models.CharField(max_length=64,unique=True)
    user_email=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)


class Links(models.Model):
    title=models.CharField(max_length=50)
    title_slug=models.CharField(max_length=50,unique=True)
    difficulty=models.CharField(max_length=10)
    tags=models.JSONField(default=list)
    url=models.URLField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    number=models.IntegerField()
    user=models.ForeignKey(User,on_delete=models.CASCADE)



