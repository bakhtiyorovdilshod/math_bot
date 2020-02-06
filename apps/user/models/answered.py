from django.db import models
from .user import User


class Answer(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	message_id = models.CharField(max_length=1000)
	choose_answer = models.CharField(max_length=100)
	number = models.IntegerField(default=0, blank=True, null=True)
	bool_answer = models.BooleanField(default=False, blank=True, null=True)

	def __str__(self):
		return str(self.user)