from django.db import models

# Create your models here.

class DjangoAdmin(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name 

class Question(models.Model):
    question = models.TextField()
    admin = models.ForeignKey(DjangoAdmin, on_delete=models.CASCADE)
    correct_option = models.ForeignKey('Option', on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

    def __str__(self):
        return self.question 
    
class Option(models.Model):
    option_description = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options') 

    def __str__(self):
        return self.option_description

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name
