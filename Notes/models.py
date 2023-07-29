from django.db import models
from django.contrib.auth.models import User 
# Create your models here.

#Signup,Notes,Contact 
#realtionship one to one 
class Signup(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    contact = models.CharField(max_length=10)
    branch = models.CharField(max_length=30)
    role = models.CharField(max_length=20)
    
    def __str__(self) -> str:
        return self.user.username
    
class Note(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    branch = models.CharField(max_length=30)
    subject = models.CharField(max_length=30)
    notesfile = models.FileField(null=True)
    filetype = models.CharField(max_length=30)
    descriptions = models.CharField(max_length=250,null=True)
    status = models.CharField(max_length=50)
    uploading_date = models.DateField(max_length=10,null=True)
    
    def __str__(self) -> str:
        return f"{self.user } = > {self.status}"
    
class Contact(models.Model):
    fullname = models.CharField(max_length=100,null=True)
    email = models.EmailField(max_length=150,null=True)
    mobile = models.CharField(max_length=20,null=True)
    subject = models.CharField(max_length=50,null=True)
    message = models.CharField(max_length=300,null=True)
    messagedate = models.DateField(max_length=10,null=True)
    isread = models.CharField(max_length=10,null=True)
    
    def __str__(self) -> str:
        return self.email
    
    
    