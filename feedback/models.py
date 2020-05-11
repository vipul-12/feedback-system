from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Feedback(models.Model):
    subject = models.CharField(max_length=20)
    review = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    punctual = models.BooleanField(default=False)
    audible = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE) #user == Student

    feedback = models.CharField(max_length=60, )

    def __str__(self):
        return self.user.username
