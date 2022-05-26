from django.db import models
from django.contrib.auth.models import  User



class UserProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    empdept = models.CharField(max_length=100, null=True)
    designation = models.CharField(max_length=100, null=True)
    contact = models.CharField(max_length=15,null=True)
    gender = models.CharField(max_length=50,null=True)
    joiningdate = models.DateTimeField(null=True)
    face_id = models.IntegerField(primary_key=True)


    def __str__(self):
        return self.user.username
