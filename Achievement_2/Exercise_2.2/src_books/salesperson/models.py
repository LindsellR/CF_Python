from django.db import models
from django.contrib.auth.models import User #needed for OneToOneField

# Create your models here.
class Salesperson(models.Model):
	username = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField(default="no bio...")
	pic = models.ImageField(upload_to='salesperson', default='no_picture.jpg')

	def __str__(self):
		return f"Profile of {self.user.username}"