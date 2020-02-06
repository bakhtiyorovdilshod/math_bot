from django.db import models


class User(models.Model):
	first_name = models.CharField(max_length=200, blank=True, null=True)
	last_name = models.CharField(max_length=200, blank=True, null=True)
	username = models.CharField(max_length=200, blank=False)
	user_id = models.CharField(max_length=200)
	numb_of_true_answer = models.IntegerField(default=0, blank=True, null=True)
	

	def __str__(self):
		return str(self.id)