from django.db import models

# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    days = models.IntegerField()
    task = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
